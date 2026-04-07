import { redirect } from "react-router";

export async function loader() {
  return redirect("/upload");
}

export default function IndexPage() {
  return null;
}
