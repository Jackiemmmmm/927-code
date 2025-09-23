import { createFileRoute } from '@tanstack/react-router'

export const Route = createFileRoute('/_layout/service-3')({
  component: RouteComponent,
})

function RouteComponent() {
  return <div>Hello "/_layout/service-3"!</div>
}
