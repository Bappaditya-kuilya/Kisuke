"use client";

import { cn } from "@/lib/utils";
import { type ButtonHTMLAttributes, forwardRef } from "react";

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "primary" | "secondary" | "ghost";
  size?: "sm" | "md" | "lg";
}

const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant = "primary", size = "md", children, ...props }, ref) => {
    return (
      <button
        ref={ref}
        className={cn(
          "inline-flex items-center justify-center font-medium transition-all duration-100",
          "focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-border-focus",
          "disabled:pointer-events-none disabled:opacity-40",
          {
            "bg-accent text-white hover:bg-accent-hover shadow-glow hover:shadow-lg rounded-full":
              variant === "primary",
            "bg-transparent text-text-primary border border-border-default hover:bg-surface-raised rounded-full":
              variant === "secondary",
            "bg-transparent text-text-secondary hover:text-text-primary hover:bg-surface-raised rounded-md":
              variant === "ghost",
          },
          {
            "h-9 px-4 text-sm gap-1.5": size === "sm",
            "h-10 px-5 text-sm gap-2": size === "md",
            "h-12 px-7 text-base gap-2.5": size === "lg",
          },
          className
        )}
        {...props}
      >
        {children}
      </button>
    );
  }
);

Button.displayName = "Button";

export { Button };
export type { ButtonProps };
