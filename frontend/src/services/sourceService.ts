export async function getSourceCount(): Promise<number> {
  try {
    const source_count_response = await fetch(
      `${process.env.NEXT_PUBLIC_API_URL}/sources/count`
    );

    if (!source_count_response.ok) {
      throw new Error(
        `Failed to fetch source count: ${source_count_response.status}`
      );
    }

    const source_count_data = await source_count_response.json();
    return source_count_data.count;
  } catch (error: unknown) {
    console.error("Error fetching source count:", error);
    return 0;
  }
}

import { Sources, SourcesResponseSchema } from "@/types/source";

export async function getSources(): Promise<Sources> {
  try {
    const sources_response = await fetch(
      `${process.env.NEXT_PUBLIC_API_URL}/sources`
    );

    if (!sources_response.ok) {
      throw new Error(`Failed to fetch sources: ${sources_response.status}`);
    }

    const sourcesData = await sources_response.json();
    const parsed = SourcesResponseSchema.parse(sourcesData);
    return parsed.sources;
  } catch (error: unknown) {
    console.error("Error fetching sources:", error);
    return [];
  }
}

export async function createSource(input: {
  source_url: string;
  tags?: string[] | null;
}): Promise<{ success: boolean; source_id?: string; error?: string }> {
  try {
    const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/sources`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        source_url: input.source_url,
        tags: input.tags ?? null,
      }),
    });

    if (!res.ok) {
      const text = await res.text();
      throw new Error(`Failed to create source: ${res.status} ${text}`);
    }

    const data = await res.json();
    return { success: true, source_id: data.source_id };
  } catch (error: unknown) {
    console.error("Error creating source:", error);
    return {
      success: false,
      error: error instanceof Error ? error.message : "Unknown error",
    };
  }
}
