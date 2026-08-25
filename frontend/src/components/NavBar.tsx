import Link from "next/link";
import { createClient } from "@/lib/supabase/server";
import { SignOutButton } from "./SignOutButton";

export async function NavBar() {
  const supabase = await createClient();
  const {
    data: { user },
  } = await supabase.auth.getUser();

  return (
    <header className="border-b border-border">
      <div className="flex items-center justify-between px-6 py-4 sm:px-10">
        <Link href="/" className="font-display text-sm font-extrabold tracking-tight">
          Verity
        </Link>

        <nav className="flex items-center gap-6">
          {user ? (
            <>
              <Link
                href="/results"
                className="text-sm font-medium text-foreground/70 hover:text-foreground"
              >
                Dashboard
              </Link>
              <Link
                href="/settings"
                className="text-sm font-medium text-foreground/70 hover:text-foreground"
              >
                Settings
              </Link>
              <SignOutButton />
            </>
          ) : (
            <>
              <Link
                href="/login"
                className="text-sm font-medium text-foreground/70 hover:text-foreground"
              >
                Log in
              </Link>
              <Link
                href="/signup"
                className="rounded-md bg-accent px-3 py-1.5 text-sm font-semibold text-accent-foreground"
              >
                Sign up
              </Link>
            </>
          )}
        </nav>
      </div>
    </header>
  );
}
