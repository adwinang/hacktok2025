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

export async function getFeatureCount(): Promise<number> {
  try {
    const feature_count_response = await fetch(
      `${process.env.NEXT_PUBLIC_API_URL}/features/count`
    );

    if (!feature_count_response.ok) {
      throw new Error(
        `Failed to fetch feature count: ${feature_count_response.status}`
      );
    }

    const feature_count_data = await feature_count_response.json();
    return feature_count_data.count;
  } catch (error: unknown) {
    console.error("Error fetching feature count:", error);
    return 0;
  }
}
