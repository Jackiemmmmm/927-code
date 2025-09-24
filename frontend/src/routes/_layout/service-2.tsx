import { createFileRoute } from "@tanstack/react-router"

export const Route = createFileRoute("/_layout/service-2")({
  component: RouteComponent,
})

function RouteComponent() {
  return <div>Hello "/_layout/service-2"!</div>
}
