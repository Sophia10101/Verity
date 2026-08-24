import { signOut } from "@/app/(auth)/actions";

export function SignOutButton() {
  return (
    <form action={signOut}>
      <button
        type="submit"
        className="text-sm font-medium text-foreground/70 hover:text-foreground"
      >
        Log out
      </button>
    </form>
  );
}
