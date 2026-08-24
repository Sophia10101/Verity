import Link from "next/link";

export default function LandingPage() {
  return (
    <div className="flex flex-1 flex-col items-center justify-center px-4 py-24 text-center">
      <h1 className="max-w-2xl text-4xl font-semibold tracking-tight text-foreground sm:text-5xl">
        A portfolio advisor that accounts for how you actually behave.
      </h1>
      <p className="mt-6 max-w-xl text-base text-foreground/60">
        Most risk questionnaires only measure what your finances can support.
        Verity also measures how you react under pressure — and shows you the
        real dollar cost of panic-selling versus staying disciplined.
      </p>
      <div className="mt-10 flex gap-4">
        <Link
          href="/signup"
          className="rounded-md bg-foreground px-5 py-2.5 text-sm font-medium text-background"
        >
          Get started
        </Link>
        <Link
          href="/login"
          className="rounded-md border border-black/10 px-5 py-2.5 text-sm font-medium text-foreground dark:border-white/15"
        >
          Log in
        </Link>
      </div>
    </div>
  );
}
