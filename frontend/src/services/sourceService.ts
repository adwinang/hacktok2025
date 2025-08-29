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
