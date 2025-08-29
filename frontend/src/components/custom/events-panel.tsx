import { Card } from "../ui/card";

export default function EventsPanel() {
  const events = [
    {
      id: 1,
      name: "Analysis completed",
      description: "No feature changes detected",
      action_required: false,
    },
    {
      id: 2,
      name: "Source backtracking",
      description: "Successfully ensured sources are up to date",
      action_required: true,
      action_link: "https://www.google.com",
    },
  ];

  return (
    <Card className="w-[480px] flex flex-col p-4 h-full sticky top-4 mt-4 mr-4">
      <div className="flex flex-col gap-2">
        <h1 className="text-lg font-bold">Real-time updates</h1>
        {events.map((event) => (
          <div key={event.id} className="flex flex-col items-start rounded-lg">
            <h2 className="text-sm font-semibold mb-0.5">{event.name}</h2>
            <p className="text-xs text-muted-foreground">{event.description}</p>
          </div>
        ))}
      </div>
    </Card>
  );
}
