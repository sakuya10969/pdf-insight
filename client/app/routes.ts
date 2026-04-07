import { type RouteConfig, index, route } from "@react-router/dev/routes";

export default [
  index("routes/index.tsx"),
  route("upload", "routes/upload.tsx"),
  route("search", "routes/search.tsx"),
  route("documents", "routes/documents.tsx"),
] satisfies RouteConfig;
