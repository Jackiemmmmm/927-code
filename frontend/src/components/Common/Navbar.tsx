import { Button, Flex, Icon, useBreakpointValue } from "@chakra-ui/react"
import { useLocation, useRouter } from "@tanstack/react-router"
import { FiArrowLeft } from "react-icons/fi"

import UserMenu from "./UserMenu"

function Navbar() {
  const display = useBreakpointValue({ base: "none", md: "flex" })
  const router = useRouter()
  const location = useLocation()

  const isDashboard = location.pathname === "/"

  const handleBackClick = () => {
    router.history.back()
  }

  return (
    <Flex
      display={display}
      justify={isDashboard ? "flex-end" : "space-between"}
      position="sticky"
      color="black"
      align="center"
      bg="bg.muted"
      w="100%"
      top={0}
      p={4}
    >
      {!isDashboard && (
        <Button
          variant="ghost"
          color="black"
          _hover={{ bg: "whiteAlpha.200" }}
          onClick={handleBackClick}
        >
          <Icon as={FiArrowLeft} />
          Back
        </Button>
      )}

      <Flex gap={2} alignItems="center">
        <UserMenu />
      </Flex>
    </Flex>
  )
}

export default Navbar
