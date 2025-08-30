import { ChartPieLabel } from "@/components/custom/pie-chart";
import { getFeatureCount, getFeatures } from "@/services/featureService";
import { transformFeaturesToChart } from "@/helpers/transformToChart";
import { NumberCard } from "@/components/custom/number-card";
import { getSourceCount } from "@/services/sourceService";
import DynamicFeaturesTable from "@/components/custom/dynamic-features-table";

export default async function Home() {
  const features = await getFeatures();
  const feature_count = await getFeatureCount();
  const source_count = await getSourceCount();

  const { data, dataKey, nameKey, chartConfig } =
    transformFeaturesToChart(features);

  // Find the status with the highest count from the features array
  const statusCounts = features.reduce<Record<string, number>>(
    (acc, feature) => {
      acc[feature.status] = (acc[feature.status] || 0) + 1;
      return acc;
    },
    {}
  );
  const status_with_highest_count = Object.entries(statusCounts).reduce(
    (maxStatus, [status, count]) =>
      count > maxStatus.count ? { status, count } : maxStatus,
    { status: "", count: 0 }
  ).status;

  return (
    <main className="flex flex-row gap-4 p-4">
      <div className="flex flex-col gap-4 flex-1">
        <div className="grid grid-cols-3 gap-4">
          <NumberCard
            title="Total Sources"
            description="Total number of sources"
            value={source_count}
            footerText="Total sources"
            href="/sources"
          // subFooterText="Total sources"
          />
          <NumberCard
            title="Total Features"
            description="Total number of features"
            value={feature_count}
            footerText="Total features"
          // subFooterText="Total features"
          />
          <ChartPieLabel
            title="Status Distribution"
            description="Features by status"
            header={
              `Majority are ${status_with_highest_count}. ` +
              (status_with_highest_count === "pass"
                ? "You're good to go!"
                : status_with_highest_count === "warning"
                  ? "Some need attention."
                  : status_with_highest_count === "pending"
                    ? "Still working on it."
                    : status_with_highest_count === "critical"
                      ? "Requires your urgent attention!"
                      : "")
            }
            subheader="Showing total composition of feature statuses"
            dataKey={dataKey}
            nameKey={nameKey}
            chartData={data}
            chartConfig={chartConfig}
          />
        </div>
        {/* <FeaturesTable data={features} /> */}
        <DynamicFeaturesTable />
      </div>
    </main>
  );
}
