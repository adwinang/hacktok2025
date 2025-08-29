import { Features, FeaturesResponseSchema } from "@/types/feature";

export async function getFeatures(): Promise<Features> {
  try {
    const features_response = await fetch(
      `${process.env.NEXT_PUBLIC_API_URL}/features`
    );

    if (!features_response.ok) {
      throw new Error(`Failed to fetch features: ${features_response.status}`);
    }

    const featuresData = await features_response.json();

    // Parse the full response structure
    const parsedResponse = FeaturesResponseSchema.parse(featuresData);

    // Return just the features array
    return parsedResponse.features;
  } catch (error: unknown) {
    console.error("Error fetching features:", error);
    return [];
  }
}
