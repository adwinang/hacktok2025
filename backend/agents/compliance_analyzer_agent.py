import os
from pathlib import Path
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel
from model.feature import Feature, FeatureStatus
from model.source_content import SourceContent
import dotenv
from pydantic import BaseModel
from typing import List, Dict

dotenv.load_dotenv()

llm = ChatAnthropic(
    model=os.getenv("ANTHROPIC_MODEL"),
    temperature=0.2,
    api_key=os.getenv("ANTHROPIC_API_KEY")
)


class ComplianceAnalyzerAgentResponse(BaseModel):
    needs_action: bool
    original_status: FeatureStatus
    status_change_to: FeatureStatus
    reason: str
    confidence: float


class ComplianceAnalyzerAgent:
    def __init__(self):
        self.structured_llm = llm.with_structured_output(
            ComplianceAnalyzerAgentResponse)

    def _format_feature_for_prompt(self, feature: Feature) -> str:
        """Format feature information for prompt injection"""
        return f"Name: {feature.name}\nDescription: {feature.description}\nCurrent Status: {feature.status}"

    def _format_source_contents_for_prompt(self, source_contents: List[SourceContent]) -> str:
        """Format source contents for prompt injection"""
        formatted_sources = []
        for i, source_content in enumerate(source_contents, 1):
            formatted_sources.append(
                f"Source {i}:\n"
                # f"Title: {source_content.title}\n"
                f"URL: {source_content.source_url}\n"
                f"Content: {source_content.content}"
            )
        return "\n\n".join(formatted_sources)

    def _create_feature_chain(self, feature: Feature, source_contents: List[SourceContent], system_template: str):
        """Create a chain for analyzing a single feature against source contents"""
        formatted_feature = self._format_feature_for_prompt(feature)
        formatted_sources = self._format_source_contents_for_prompt(
            source_contents)

        chat_prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content=system_template),
            HumanMessage(content="Feature to Analyze:\n{feature_details}"),
            HumanMessage(
                content="Regulatory Source Content:\n{source_content}")
        ])

        chain = chat_prompt | self.structured_llm

        # Return a lambda that will invoke the chain with the formatted data
        return lambda: chain.ainvoke({
            "feature_details": formatted_feature,
            "source_content": formatted_sources
        })

    async def analyze_compliance(self, source_contents: List[SourceContent], features: List[Feature]) -> List[ComplianceAnalyzerAgentResponse]:
        """Analyze multiple features compliance against regulatory source requirements in parallel"""
        try:
            # Load system prompt template
            current_dir = Path(__file__).parent
            template_path = current_dir / "templates" / "compliance_analyzer.md"
            system_template_content = template_path.read_text(encoding='utf-8')

            # Create chains for each feature
            chains_dict = {}
            for i, feature in enumerate(features):
                chain_key = f"feature_{i}_{feature.id}" if feature.id else f"feature_{i}"

                # Create individual chat prompt for this feature
                formatted_feature = self._format_feature_for_prompt(feature)
                formatted_sources = self._format_source_contents_for_prompt(
                    source_contents)

                chat_prompt = ChatPromptTemplate.from_messages([
                    SystemMessage(content=system_template_content),
                    HumanMessage(
                        content="Feature to Analyze:\n{feature_details}"),
                    HumanMessage(
                        content="Regulatory Source Content:\n{source_content}")
                ])

                # Create chain for this specific feature
                chain = chat_prompt | self.structured_llm

                # Store the chain with pre-formatted data
                chains_dict[chain_key] = chain.with_config(
                    {"configurable": {
                        "feature_details": formatted_feature,
                        "source_content": formatted_sources
                    }}
                )

            # Create parallel runnable
            parallel_runnable = RunnableParallel(**chains_dict)

            # Execute all chains in parallel
            # We need to create the input data for each chain
            parallel_input = {}
            for i, feature in enumerate(features):
                chain_key = f"feature_{i}_{feature.id}" if feature.id else f"feature_{i}"
                formatted_feature = self._format_feature_for_prompt(feature)
                formatted_sources = self._format_source_contents_for_prompt(
                    source_contents)
                parallel_input[chain_key] = {
                    "feature_details": formatted_feature,
                    "source_content": formatted_sources
                }

            # Actually, let's simplify this - create individual chains and run them in parallel
            chains_dict_simple = {}
            for i, feature in enumerate(features):
                chain_key = f"feature_{i}_{feature.id}" if feature.id else f"feature_{i}"
                formatted_feature = self._format_feature_for_prompt(feature)
                formatted_sources = self._format_source_contents_for_prompt(
                    source_contents)

                chat_prompt = ChatPromptTemplate.from_messages([
                    SystemMessage(content=system_template_content),
                    HumanMessage(
                        content=f"Feature to Analyze:\n{formatted_feature}"),
                    HumanMessage(
                        content=f"Regulatory Source Content:\n{formatted_sources}")
                ])

                chains_dict_simple[chain_key] = chat_prompt | self.structured_llm

            # Create parallel runnable and execute
            parallel_runnable = RunnableParallel(**chains_dict_simple)
            results_dict = await parallel_runnable.ainvoke({})

            # Convert results dict to list maintaining feature order
            results_list = []
            for i, feature in enumerate(features):
                chain_key = f"feature_{i}_{feature.id}" if feature.id else f"feature_{i}"
                results_list.append(results_dict[chain_key])

            return results_list

        except FileNotFoundError as e:
            raise FileNotFoundError(f"Template file not found: {e}")
        except Exception as e:
            raise RuntimeError(f"Error analyzing compliance: {e}")
