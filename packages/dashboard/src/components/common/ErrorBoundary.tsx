/**
 * Error Boundary Component
 * AFO Kingdom Dashboard - Error Boundary with Context7 Best Practices
 * 
 * Based on Next.js App Router error handling patterns
 */

"use client";

import React, { Component, ErrorInfo, ReactNode } from "react";
import { AlertTriangle, RefreshCw } from "lucide-react";

interface ErrorBoundaryProps {
  children: ReactNode;
  fallback?: ReactNode;
  onError?: (error: Error, errorInfo: ErrorInfo) => void;
  resetKeys?: Array<string | number>;
  resetOnPropsChange?: boolean;
}

interface ErrorBoundaryState {
  hasError: boolean;
  error: Error | null;
  errorInfo: ErrorInfo | null;
}

export class ErrorBoundary extends Component<
  ErrorBoundaryProps,
  ErrorBoundaryState
> {
  constructor(props: ErrorBoundaryProps) {
    super(props);
    this.state = {
      hasError: false,
      error: null,
      errorInfo: null,
    };
  }

  static getDerivedStateFromError(error: Error): Partial<ErrorBoundaryState> {
    return {
      hasError: true,
      error,
    };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    // Log error to error reporting service
    console.error("ErrorBoundary caught an error:", error, errorInfo);

    this.setState({
      error,
      errorInfo,
    });

    // Call custom error handler if provided
    if (this.props.onError) {
      this.props.onError(error, errorInfo);
    }
  }

  componentDidUpdate(
    prevProps: ErrorBoundaryProps,
    _prevState: ErrorBoundaryState
  ) {
    const { resetKeys, resetOnPropsChange } = this.props;
    const { hasError } = this.state;

    // Reset error boundary if resetKeys change
    if (hasError && resetKeys) {
      const hasResetKeyChanged = resetKeys.some(
        (key, index) => key !== prevProps.resetKeys?.[index]
      );
      if (hasResetKeyChanged) {
        this.resetErrorBoundary();
      }
    }

    // Reset on props change if enabled
    if (hasError && resetOnPropsChange) {
      const hasPropsChanged = Object.keys(this.props).some(
        (key) =>
          key !== "children" &&
          key !== "fallback" &&
          key !== "onError" &&
          key !== "resetKeys" &&
          key !== "resetOnPropsChange" &&
          this.props[key as keyof ErrorBoundaryProps] !==
            prevProps[key as keyof ErrorBoundaryProps]
      );
      if (hasPropsChanged) {
        this.resetErrorBoundary();
      }
    }
  }

  resetErrorBoundary = () => {
    this.setState({
      hasError: false,
      error: null,
      errorInfo: null,
    });
  };

  render() {
    if (this.state.hasError) {
      // Use custom fallback if provided
      if (this.props.fallback) {
        return this.props.fallback;
      }

      // Default fallback UI
      return (
        <div
          role="alert"
          aria-live="assertive"
          aria-atomic="true"
          className="bg-red-900/20 border border-red-500/50 rounded-lg p-6 min-h-[200px] flex items-center justify-center"
        >
          <div className="text-center max-w-md">
            <AlertTriangle
              className="w-12 h-12 text-red-400 mx-auto mb-4"
              aria-hidden="true"
            />
            <h2 className="text-red-300 text-xl font-semibold mb-2">
              Something went wrong
            </h2>
            <p className="text-red-400 text-sm mb-4">
              {this.state.error?.message || "An unexpected error occurred"}
            </p>
            {process.env.NODE_ENV === "development" && this.state.errorInfo && (
              <details className="text-left mb-4">
                <summary className="text-red-300 text-sm cursor-pointer mb-2">
                  Error Details (Development Only)
                </summary>
                <pre className="text-xs text-red-400 bg-red-950/30 p-3 rounded overflow-auto max-h-40">
                  {this.state.error?.stack}
                </pre>
              </details>
            )}
            <button
              onClick={this.resetErrorBoundary}
              className="px-4 py-2 bg-red-600 hover:bg-red-700 rounded-lg text-white text-sm font-medium flex items-center gap-2 transition-colors mx-auto"
              aria-label="Try again to reload the component"
            >
              <RefreshCw className="w-4 h-4" aria-hidden="true" />
              Try again
            </button>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}

export default ErrorBoundary;

