import Link from "next/link";
import { createClient } from "@/lib/supabase/server";
import { SignOutButton } from "./SignOutButton";

export async function NavBar() {
  const supabase = await createClient();
  const {
    data: { user },
  } = await supabase.auth.getUser();

  return (
    <header className="border-b border-black/10 dark:border-white/10">
      <div className="mx-auto flex max-w-5xl items-center justify-between px-4 py-4">
        <Link href="/" className="text-sm font-semibold tracking-tight">
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
                className="rounded-md bg-foreground px-3 py-1.5 text-sm font-medium text-background"
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
