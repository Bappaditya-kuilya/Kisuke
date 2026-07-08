import Link from "next/link";
import { ChevronRight } from "lucide-react";

interface BreadcrumbItem {
  label: string;
  href?: string;
}

interface BreadcrumbsProps {
  items: BreadcrumbItem[];
}

function Breadcrumbs({ items }: BreadcrumbsProps) {
  return (
    <nav aria-label="Breadcrumb" className="mb-8">
      <ol className="flex items-center gap-1.5 text-sm">
        <li>
          <Link
            href="/"
            className="text-text-tertiary hover:text-text-primary transition-colors duration-100"
          >
            Home
          </Link>
        </li>
        {items.map((item) => (
          <li key={item.label} className="flex items-center gap-1.5">
            <ChevronRight className="w-3.5 h-3.5 text-text-disabled" />
            {item.href ? (
              <Link
                href={item.href}
                className="text-text-tertiary hover:text-text-primary transition-colors duration-100"
              >
                {item.label}
              </Link>
            ) : (
              <span className="text-text-secondary">{item.label}</span>
            )}
          </li>
        ))}
      </ol>
    </nav>
  );
}

export { Breadcrumbs };
