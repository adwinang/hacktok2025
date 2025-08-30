"use client";
import { useEffect, useReducer, useRef } from "react";
import SourcesTable from "@/components/custom/sources-table";
import { Sources, Source } from "@/types/source";
import { SourceStreamEventSchema } from "@/types/source";

type SourcesState = {
    sources: Sources;
    loading: boolean;
    error: string | null;
};

type SourcesAction =
    | { type: "LOADING" }
    | { type: "SET_INITIAL_SOURCES"; payload: Sources }
    | { type: "UPSERT_SOURCE"; payload: { sourceId: string; sourceData: Source } }
    | { type: "ERROR"; payload: string }
    | { type: "RESET_ERROR" };

function sourcesReducer(state: SourcesState, action: SourcesAction): SourcesState {
    switch (action.type) {
        case "LOADING":
            return { ...state, loading: true, error: null };
        case "SET_INITIAL_SOURCES":
            return { sources: action.payload, loading: false, error: null };
        case "UPSERT_SOURCE": {
            const { sourceId, sourceData } = action.payload;
            const exists = state.sources.some((s) => s.id === sourceId);
            const updated = exists
                ? state.sources.map((s) => (s.id === sourceId ? sourceData : s))
                : [sourceData, ...state.sources];
            return { ...state, sources: updated };
        }
        case "ERROR":
            return { ...state, loading: false, error: action.payload };
        case "RESET_ERROR":
            return { ...state, error: null };
        default:
            return state;
    }
}

export default function DynamicSourcesTable() {
    const [state, dispatch] = useReducer(sourcesReducer, {
        sources: [],
        loading: true,
        error: null,
    });

    const eventSourceRef = useRef<EventSource | null>(null);

    useEffect(() => {
        dispatch({ type: "LOADING" });
        const eventSource = new EventSource(`${process.env.NEXT_PUBLIC_API_URL}/sources/stream`);
        eventSourceRef.current = eventSource;

        eventSource.onmessage = (event) => {
            try {
                const parsed = JSON.parse(event.data);
                const validated = SourceStreamEventSchema.parse(parsed);
                if (validated.type === "initial_data") {
                    dispatch({ type: "SET_INITIAL_SOURCES", payload: validated.data.sources });
                } else if (validated.type === "source_update") {
                    dispatch({
                        type: "UPSERT_SOURCE",
                        payload: { sourceId: validated.data.source_id, sourceData: validated.data.source_data },
                    });
                } else if (validated.type === "error") {
                    dispatch({ type: "ERROR", payload: validated.data.message });
                }
            } catch (error) {
                console.error("Error parsing or validating source stream event:", error);
                dispatch({
                    type: "ERROR",
                    payload: `Failed to parse stream event: ${error instanceof Error ? error.message : "Unknown error"}`,
                });
            }
        };

        eventSource.onerror = (error) => {
            console.error("Source EventSource error:", error);
            dispatch({ type: "ERROR", payload: "Connection to source stream failed" });
        };

        eventSource.onopen = () => {
            dispatch({ type: "RESET_ERROR" });
        };

        return () => {
            if (eventSourceRef.current) {
                eventSourceRef.current.close();
                eventSourceRef.current = null;
            }
        };
    }, []);

    if (state.error) {
        return (
            <div className="p-4 text-center">
                <p className="text-red-600 mb-2">Error loading sources: {state.error}</p>
                <button
                    onClick={() => window.location.reload()}
                    className="px-4 py-2 bg-red-100 text-red-700 rounded hover:bg-red-200"
                >
                    Retry
                </button>
            </div>
        );
    }

    if (state.loading) {
        return (
            <div className="p-4 text-center">
                <p>Loading sources...</p>
            </div>
        );
    }

    return <SourcesTable data={state.sources} />;
}


