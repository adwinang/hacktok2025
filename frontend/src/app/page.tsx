import { ChartPieLabel } from "@/components/custom/pie-chart";
import { getFeatureCount, getFeatures } from "@/services/featureService";
import FeaturesTable from "@/components/custom/features-table";
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

  return (
    <main className="flex flex-row gap-4 p-4">
      <div className="flex flex-col gap-4 flex-1">
        <div className="grid grid-cols-3 gap-4">
          <NumberCard
            title="Total Sources"
            description="Total number of sources"
            value={source_count}
            footerText="Total sources"
            subFooterText="Total sources"
          />
          <NumberCard
            title="Total Features"
            description="Total number of features"
            value={feature_count}
            footerText="Total features"
            subFooterText="Total features"
          />
          <ChartPieLabel
            title="Status Distribution"
            description="Features by status"
            header="Trending up by 5.2% this month"
            subheader="Showing total visitors for the last 6 months"
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
