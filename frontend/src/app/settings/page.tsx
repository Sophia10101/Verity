import Link from "next/link";
import { createClient } from "@/lib/supabase/server";

export default async function SettingsPage() {
  const supabase = await createClient();
  const {
    data: { user },
  } = await supabase.auth.getUser();

  return (
    <div className="mx-auto w-full max-w-lg px-4 py-16">
      <h1 className="text-2xl font-semibold text-foreground">Account settings</h1>

      <dl className="mt-8 space-y-4">
        <div>
          <dt className="text-xs text-foreground/50">Email</dt>
          <dd className="text-sm text-foreground">{user?.email}</dd>
        </div>
        <div>
          <dt className="text-xs text-foreground/50">Member since</dt>
          <dd className="text-sm text-foreground">
            {user?.created_at
              ? new Date(user.created_at).toLocaleDateString()
              : "—"}
          </dd>
        </div>
      </dl>

      <div className="mt-8 space-y-2">
        <Link
          href="/financial-profile"
          className="block text-sm font-medium text-foreground underline"
        >
          Update financial profile
        </Link>
        <Link
          href="/questionnaire"
          className="block text-sm font-medium text-foreground underline"
        >
          Retake behavioral questionnaire
        </Link>
      </div>
    </div>
  );
}
