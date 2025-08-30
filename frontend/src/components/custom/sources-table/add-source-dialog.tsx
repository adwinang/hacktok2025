"use client";
import { useState, useTransition } from "react";
import { useRouter } from "next/navigation";
import { Dialog, DialogContent, DialogFooter, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { createSource } from "@/services/sourceService";

export default function AddSourceDialog({ onCreated }: { onCreated?: () => void }) {
    const router = useRouter();
    const [open, setOpen] = useState(false);
    const [url, setUrl] = useState("");
    const [error, setError] = useState<string | null>(null);
    const [isPending, startTransition] = useTransition();

    function handleSubmit() {
        setError(null);
        if (!url.trim()) {
            setError("Source URL is required");
            return;
        }
        startTransition(async () => {
            const result = await createSource({
                source_url: url.trim(),
            });
            if (!result.success) {
                setError(result.error ?? "Failed to create source");
                return;
            }
            setOpen(false);
            setUrl("");
            // Refresh server components (re-fetch sources)
            router.refresh();
            onCreated?.();
        });
    }

    return (
        <Dialog open={open} onOpenChange={setOpen}>
            <DialogTrigger asChild>
                <Button>Add Source</Button>
            </DialogTrigger>
            <DialogContent>
                <DialogHeader>
                    <DialogTitle>Add Source</DialogTitle>
                </DialogHeader>
                <div className="space-y-4 py-2">
                    <div className="space-y-2">
                        <label htmlFor="url" className="text-sm font-medium">
                            Source URL
                        </label>
                        <Input
                            id="url"
                            placeholder="https://example.com/article"
                            value={url}
                            onChange={(e) => setUrl(e.target.value)}
                        />
                    </div>
                    {error && <p className="text-sm text-red-600">{error}</p>}
                </div>
                <DialogFooter>
                    <Button variant="outline" onClick={() => setOpen(false)} disabled={isPending}>
                        Cancel
                    </Button>
                    <Button onClick={handleSubmit} disabled={isPending}>
                        {isPending ? "Creating..." : "Create"}
                    </Button>
                </DialogFooter>
            </DialogContent>
        </Dialog>
    );
}


