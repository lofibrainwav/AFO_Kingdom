"use client";

import * as React from "react";

const Alert = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement> & { variant?: "default" | "destructive" }
>(({ className = "", variant = "default", ...props }, ref) => {
  const variantStyles =
    variant === "destructive"
      ? "border-red-500/50 text-red-600 bg-red-50"
      : "border-slate-200 text-slate-700 bg-slate-50";

  return (
    <div
      ref={ref}
      role="alert"
      className={`relative w-full rounded-lg border p-4 ${variantStyles} ${className}`}
      {...props}
    />
  );
});
Alert.displayName = "Alert";

const AlertTitle = React.forwardRef<
  HTMLHeadingElement,
  React.HTMLAttributes<HTMLHeadingElement>
>(({ className = "", ...props }, ref) => (
  <h5
    ref={ref}
    className={`mb-1 font-medium leading-none tracking-tight ${className}`}
    {...props}
  />
));
AlertTitle.displayName = "AlertTitle";

const AlertDescription = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement>
>(({ className = "", ...props }, ref) => (
  <div
    ref={ref}
    className={`text-sm opacity-90 ${className}`}
    {...props}
  />
));
AlertDescription.displayName = "AlertDescription";

export { Alert, AlertTitle, AlertDescription };
