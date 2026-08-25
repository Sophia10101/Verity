import Link from "next/link";

export default function LandingPage() {
  return (
    <div className="flex flex-1 flex-col items-center justify-center px-6 py-32 text-center sm:py-40">
      <h1 className="max-w-3xl font-display text-5xl font-extrabold tracking-tight text-balance sm:text-6xl lg:text-7xl">
        Your biggest risk isn&apos;t the market. It&apos;s{" "}
        <span className="text-accent">how you&apos;ll react to it</span>.
      </h1>
      <p className="mt-8 max-w-2xl text-lg leading-relaxed text-muted">
        It&apos;s called the behavior gap: decades of research from DALBAR and
        Morningstar show investors consistently earn less than the funds
        they&apos;re invested in, not from bad picks, but from panic-selling
        in crashes and buying back in after they&apos;ve recovered. Most
        tools only look at what your finances can support. Verity combines
        that with your psychological profile, estimates what your own
        reactions might cost you, and builds a portfolio designed to account
        for both.
      </p>
      <div className="mt-12 flex gap-4">
        <Link
          href="/signup"
          className="rounded-md bg-accent px-6 py-3 text-base font-semibold text-accent-foreground"
        >
          Get started
        </Link>
        <Link
          href="/login"
          className="rounded-md border border-foreground/20 px-6 py-3 text-base font-semibold text-foreground/80"
        >
          Log in
        </Link>
      </div>
    </div>
  );
}
