import AddSourceButton from "./add-source-button";

export default function SourcesLayout({
    children,
}: {
    children: React.ReactNode;
}) {
    return (
        <div className="p-4 w-full">
            <div className="mb-6 flex items-start justify-between gap-4">
                <div>
                    <h1 className="text-2xl font-semibold tracking-tight">Sources</h1>
                    <p className="text-sm text-muted-foreground">
                        Browse and manage all content sources powering your knowledge base.
                    </p>
                </div>
                {/* Add Source dialog trigger */}
                <AddSourceButton />
            </div>
            {children}
        </div>
    );
}


