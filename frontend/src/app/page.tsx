import { ChartPieLabel } from "@/components/custom/pie-chart";
import { getFeatures } from "@/services/featureService";
import FeaturesTable from "@/components/custom/features-table";
import { transformFeaturesToChart } from "@/helpers/transformToChart";
import { NumberCard } from "@/components/custom/number-card";

export default async function Home() {
  const features = await getFeatures();

  const { data, dataKey, nameKey, chartConfig } =
    transformFeaturesToChart(features);

  return (
    <main className="flex flex-row gap-4 p-4">
      <div className="flex flex-col gap-4 flex-1">
        <div className="grid grid-cols-3 gap-4">
          <NumberCard
            title="Total Sources"
            description="Total number of sources"
            value={100}
            footerText="Total sources"
            subFooterText="Total sources"
          />
          <NumberCard
            title="Total Features"
            description="Total number of features"
            value={1412}
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
        <FeaturesTable data={features} />
      </div>
    </main>
  );
}
