import { cn } from "@/lib/utils";

interface SectionProps {
  children: React.ReactNode;
  className?: string;
  id?: string;
}

function Section({ children, className, id }: SectionProps) {
  return (
    <section
      id={id}
      className={cn("py-24 px-6 md:px-8 lg:px-0", className)}
    >
      <div className="mx-auto max-w-[1200px]">{children}</div>
    </section>
  );
}

export { Section };
