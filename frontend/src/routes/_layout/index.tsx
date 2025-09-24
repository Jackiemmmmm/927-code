import {
  Box,
  Container,
  Flex,
  Heading,
  Icon,
  SimpleGrid,
  Text,
} from "@chakra-ui/react"
import { createFileRoute, Link } from "@tanstack/react-router"
import { FiActivity, FiBriefcase, FiFilter } from "react-icons/fi"

import useAuth from "@/hooks/useAuth"

export const Route = createFileRoute("/_layout/")({
  component: Dashboard,
})

const services = [
  {
    icon: FiActivity,
    title: "Medical Appointment Booking Service",
    path: "/service-1",
    color: "blue.500",
  },
  {
    icon: FiFilter,
    title: "Online Tax Refund Application",
    path: "/service-2",
    color: "green.500",
  },
  {
    icon: FiBriefcase,
    title: "Application Record Query",
    path: "/service-3",
    color: "purple.500",
  },
]

function Dashboard() {
  const { user: currentUser } = useAuth()

  return (
    <Container maxW="full">
      <Box pt={12} m={4}>
        <Text fontSize="2xl" truncate maxW="sm">
          Hi, {currentUser?.full_name || currentUser?.email} 👋🏼
        </Text>
        <Text mb={8}>Welcome back, nice to see you again!</Text>

        <Heading size="lg" mb={6}>
          Service Center
        </Heading>

        <SimpleGrid columns={{ base: 1, md: 2, lg: 3 }} gap={6}>
          {services.map((service) => (
            <Link key={service.path} to={service.path}>
              <Box
                p={6}
                borderWidth="1px"
                borderRadius="lg"
                bg="white"
                _hover={{
                  transform: "translateY(-4px)",
                  shadow: "lg",
                  transition: "all 0.2s",
                }}
                cursor="pointer"
                transition="all 0.2s"
                h="full"
              >
                <Flex direction="column" align="center" textAlign="center">
                  <Icon
                    as={service.icon}
                    boxSize={12}
                    color={service.color}
                    mb={4}
                  />
                  <Heading size="md" mb={2}>
                    {service.title}
                  </Heading>
                </Flex>
              </Box>
            </Link>
          ))}
        </SimpleGrid>
      </Box>
    </Container>
  )
}
