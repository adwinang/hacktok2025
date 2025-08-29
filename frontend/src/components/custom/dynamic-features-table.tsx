"use client";

import { useEffect, useReducer, useRef } from "react";
import FeaturesTable from "./features-table";
import { Features, StreamEventSchema, Feature } from "@/types/feature";

type FeaturesState = {
  features: Features;
  loading: boolean;
  error: string | null;
};

type FeaturesAction =
  | { type: "LOADING" }
  | { type: "SET_INITIAL_FEATURES"; payload: Features }
  | {
      type: "UPDATE_FEATURE";
      payload: { featureId: string; featureData: Feature };
    }
  | { type: "ERROR"; payload: string }
  | { type: "RESET_ERROR" };

function featuresReducer(
  state: FeaturesState,
  action: FeaturesAction
): FeaturesState {
  switch (action.type) {
    case "LOADING":
      return { ...state, loading: true, error: null };

    case "SET_INITIAL_FEATURES":
      return {
        features: action.payload,
        loading: false,
        error: null,
      };

    case "UPDATE_FEATURE":
      const { featureId, featureData } = action.payload;
      const updatedFeatures = state.features.map((feature) =>
        feature.id === featureId ? featureData : feature
      );
      return {
        ...state,
        features: updatedFeatures,
      };

    case "ERROR":
      return {
        ...state,
        loading: false,
        error: action.payload,
      };

    case "RESET_ERROR":
      return {
        ...state,
        error: null,
      };

    default:
      return state;
  }
}

export default function DynamicFeaturesTable() {
  const [state, dispatch] = useReducer(featuresReducer, {
    features: [],
    loading: true,
    error: null,
  });

  const eventSourceRef = useRef<EventSource | null>(null);

  useEffect(() => {
    dispatch({ type: "LOADING" });

    // Create SSE connection
    const eventSource = new EventSource(
      `${process.env.NEXT_PUBLIC_API_URL}/features/stream`
    );

    eventSourceRef.current = eventSource;

    eventSource.onmessage = (event) => {
      try {
        // Parse and validate the event data
        const eventData = JSON.parse(event.data);
        const validatedEvent = StreamEventSchema.parse(eventData);

        if (validatedEvent.type === "initial_data") {
          dispatch({
            type: "SET_INITIAL_FEATURES",
            payload: validatedEvent.data.features,
          });
        } else if (validatedEvent.type === "feature_update") {
          dispatch({
            type: "UPDATE_FEATURE",
            payload: {
              featureId: validatedEvent.data.feature_id,
              featureData: validatedEvent.data.feature_data,
            },
          });
        } else if (validatedEvent.type === "error") {
          dispatch({
            type: "ERROR",
            payload: validatedEvent.data.message,
          });
        }
      } catch (error) {
        console.error("Error parsing or validating event data:", error);
        dispatch({
          type: "ERROR",
          payload: `Failed to parse stream event: ${
            error instanceof Error ? error.message : "Unknown error"
          }`,
        });
      }
    };

    eventSource.onerror = (error) => {
      console.error("EventSource error:", error);
      dispatch({
        type: "ERROR",
        payload: "Connection to feature stream failed",
      });
    };

    eventSource.onopen = () => {
      console.log("EventSource connection opened");
      dispatch({ type: "RESET_ERROR" });
    };

    // Cleanup function
    return () => {
      if (eventSourceRef.current) {
        eventSourceRef.current.close();
        eventSourceRef.current = null;
      }
    };
  }, []); // Empty dependency array is correct here

  // Handle error state
  if (state.error) {
    return (
      <div className="p-4 text-center">
        <p className="text-red-600 mb-2">
          Error loading features: {state.error}
        </p>
        <button
          onClick={() => window.location.reload()}
          className="px-4 py-2 bg-red-100 text-red-700 rounded hover:bg-red-200"
        >
          Retry
        </button>
      </div>
    );
  }

  // Handle loading state
  if (state.loading) {
    return (
      <div className="p-4 text-center">
        <p>Loading features...</p>
      </div>
    );
  }

  return <FeaturesTable data={state.features} />;
}
