import {
  Alert,
  Badge,
  Box,
  Container,
  Heading,
  HStack,
  Input,
  Separator,
  SimpleGrid,
  Stack,
  Text,
} from "@chakra-ui/react"
import { useMutation, useQuery } from "@tanstack/react-query"
import { createFileRoute } from "@tanstack/react-router"
import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Field } from "@/components/ui/field"
import { toaster } from "@/components/ui/toaster"
import { AppointmentsService } from "@/client"
import type {
  AppointmentCreate,
  UserValidation,
} from "@/client"

export const Route = createFileRoute("/_layout/service-1")({
  component: RouteComponent,
})

interface UserInfo {
  name: string
  idNumber: string
  phone: string
  email: string
}

function RouteComponent() {
  const [currentStep, setCurrentStep] = useState(1)
  const [userInfo, setUserInfo] = useState<UserInfo>({
    name: "",
    idNumber: "",
    phone: "",
    email: "",
  })
  const [selectedHospital, setSelectedHospital] = useState("")
  const [selectedDoctor, setSelectedDoctor] = useState("")
  const [selectedTime, setSelectedTime] = useState("")
  const [error, setError] = useState("")

  // Fetch hospitals
  const { data: hospitalsData } = useQuery({
    queryKey: ["hospitals"],
    queryFn: () => AppointmentsService.getHospitals(),
  })

  // Fetch doctors for selected hospital
  const { data: doctorsData } = useQuery({
    queryKey: ["doctors", selectedHospital],
    queryFn: () =>
      AppointmentsService.getHospitalDoctors({
        hospitalId: selectedHospital,
      }),
    enabled: !!selectedHospital,
  })

  // Fetch time slots for selected doctor
  const { data: timeSlotsData } = useQuery({
    queryKey: ["timeSlots", selectedDoctor],
    queryFn: () =>
      AppointmentsService.getDoctorTimeSlots({
        doctorId: selectedDoctor,
      }),
    enabled: !!selectedDoctor,
  })

  // Validate user mutation
  const validateUserMutation = useMutation({
    mutationFn: (userValidation: UserValidation) =>
      AppointmentsService.validateUser({
        requestBody: userValidation,
      }),
    onSuccess: () => {
      setCurrentStep(2)
      setError("")
    },
    onError: (err: any) => {
      setError(
        err.body?.detail || "User validation failed. Please check your information and try again.",
      )
    },
  })

  // Create appointment mutation
  const createAppointmentMutation = useMutation({
    mutationFn: (appointmentData: AppointmentCreate) =>
      AppointmentsService.createAppointment({
        requestBody: appointmentData,
      }),
    onSuccess: (data) => {
      const doctor = doctorsData?.data.find((d) => d.id === selectedDoctor)
      toaster.create({
        title: "Appointment Booked Successfully!",
        description: `Your appointment with ${doctor?.name} at ${selectedTime} has been confirmed.`,
        type: "success",
      })
      // Reset form
      setCurrentStep(1)
      setUserInfo({ name: "", idNumber: "", phone: "", email: "" })
      setSelectedHospital("")
      setSelectedDoctor("")
      setSelectedTime("")
      setError("")
    },
    onError: (err: any) => {
      setError(err.body?.detail || "Booking failed. Please try again.")
    },
  })

  const handleUserInfoSubmit = async () => {
    setError("")
    validateUserMutation.mutate({
      name: userInfo.name,
      id_number: userInfo.idNumber,
      phone: userInfo.phone,
      email: userInfo.email || undefined,
    })
  }

  const handleHospitalSelect = (hospitalId: string) => {
    setSelectedHospital(hospitalId)
    setSelectedDoctor("")
    setSelectedTime("")
    setCurrentStep(3)
  }

  const handleDoctorSelect = (doctorId: string) => {
    setSelectedDoctor(doctorId)
    setSelectedTime("")
    setCurrentStep(4)
  }

  const handleTimeSelect = (time: string) => {
    setSelectedTime(time)
    setCurrentStep(5)
  }

  const handleConfirmBooking = async () => {
    setError("")
    createAppointmentMutation.mutate({
      patient_name: userInfo.name,
      patient_id_number: userInfo.idNumber,
      patient_phone: userInfo.phone,
      patient_email: userInfo.email || undefined,
      appointment_time: selectedTime,
      hospital_id: selectedHospital,
      doctor_id: selectedDoctor,
    })
  }

  const renderStep1 = () => (
    <Stack gap={6} align="stretch">
      <Heading size="lg">Step 1: User Information</Heading>
      <Stack gap={4}>
        <Field label="Full Name" required>
          <Input
            value={userInfo.name}
            onChange={(e) => setUserInfo({ ...userInfo, name: e.target.value })}
            placeholder="Enter your full name"
          />
        </Field>
        <Field label="ID Number" required>
          <Input
            value={userInfo.idNumber}
            onChange={(e) =>
              setUserInfo({ ...userInfo, idNumber: e.target.value })
            }
            placeholder="Enter your ID number"
          />
        </Field>
        <Field label="Phone Number" required>
          <Input
            value={userInfo.phone}
            onChange={(e) =>
              setUserInfo({ ...userInfo, phone: e.target.value })
            }
            placeholder="Enter your phone number"
          />
        </Field>
        <Field label="Email">
          <Input
            type="email"
            value={userInfo.email}
            onChange={(e) =>
              setUserInfo({ ...userInfo, email: e.target.value })
            }
            placeholder="Enter your email (optional)"
          />
        </Field>
        {error && (
          <Alert.Root status="error">
            <Alert.Indicator />
            <Alert.Title>{error}</Alert.Title>
          </Alert.Root>
        )}
        <Button
          colorScheme="blue"
          onClick={handleUserInfoSubmit}
          loading={validateUserMutation.isPending}
          loadingText="Validating..."
          size="lg"
          w="full"
        >
          Submit Information
        </Button>
      </Stack>
    </Stack>
  )

  const renderStep2 = () => (
    <Stack gap={6} align="stretch">
      <Heading size="lg">Step 2: Select Hospital</Heading>
      <SimpleGrid columns={{ base: 1, md: 2 }} gap={4}>
        {hospitalsData?.data.map((hospital) => (
          <Box
            key={hospital.id}
            p={6}
            borderWidth="1px"
            borderRadius="lg"
            cursor="pointer"
            _hover={{ shadow: "md" }}
            onClick={() => handleHospitalSelect(hospital.id)}
          >
            <Heading size="md" mb={2}>
              {hospital.name}
            </Heading>
            <Text color="gray.600">{hospital.address}</Text>
          </Box>
        ))}
      </SimpleGrid>
      <Button variant="outline" onClick={() => setCurrentStep(1)}>
        Back to User Information
      </Button>
    </Stack>
  )

  const renderStep3 = () => (
    <Stack gap={6} align="stretch">
      <Heading size="lg">Step 3: Select Doctor</Heading>
      <Text>
        Hospital: {hospitalsData?.data.find((h) => h.id === selectedHospital)?.name}
      </Text>
      <SimpleGrid columns={{ base: 1, md: 2 }} gap={4}>
        {doctorsData?.data.map(
          (doctor) => (
            <Box
              key={doctor.id}
              p={6}
              borderWidth="1px"
              borderRadius="lg"
              cursor="pointer"
              _hover={{ shadow: "md" }}
              onClick={() => handleDoctorSelect(doctor.id)}
            >
              <Heading size="md" mb={2}>
                {doctor.name}
              </Heading>
              <HStack justify="space-between" mb={2}>
                <Text color="gray.600">{doctor.specialty}</Text>
                <Badge colorScheme="green">★ {doctor.rating}</Badge>
              </HStack>
            </Box>
          ),
        )}
      </SimpleGrid>
      <Button variant="outline" onClick={() => setCurrentStep(2)}>
        Back to Hospital Selection
      </Button>
    </Stack>
  )

  const renderStep4 = () => {
    const doctor = doctorsData?.data.find((d) => d.id === selectedDoctor)
    const availableTimes = timeSlotsData || []

    return (
      <Stack gap={6} align="stretch">
        <Heading size="lg">Step 4: Select Appointment Time</Heading>
        <Box>
          <Text mb={2}>Doctor: {doctor?.name}</Text>
          <Text mb={4} color="gray.600">
            Specialty: {doctor?.specialty}
          </Text>
        </Box>
        <Separator />
        <Heading size="md">Available Times</Heading>
        {availableTimes.length > 0 ? (
          <SimpleGrid columns={{ base: 2, md: 4 }} gap={4}>
            {availableTimes.map((slot) => (
              <Button
                key={slot.id}
                variant="outline"
                onClick={() => handleTimeSelect(slot.time_slot)}
                _hover={{ bg: "blue.50" }}
              >
                {slot.time_slot}
              </Button>
            ))}
          </SimpleGrid>
        ) : (
          <Alert.Root status="info">
            <Alert.Indicator />
            <Alert.Title>
              No available times for this doctor. Please select a different
              doctor.
            </Alert.Title>
          </Alert.Root>
        )}
        <Button variant="outline" onClick={() => setCurrentStep(3)}>
          Back to Doctor Selection
        </Button>
      </Stack>
    )
  }

  const renderStep5 = () => {
    const hospital = hospitalsData?.data.find((h) => h.id === selectedHospital)
    const doctor = doctorsData?.data.find((d) => d.id === selectedDoctor)

    return (
      <Stack gap={6} align="stretch">
        <Heading size="lg">Step 5: Confirm Appointment</Heading>
        <Box p={6} borderWidth="1px" borderRadius="lg">
          <Stack gap={3} align="stretch">
            <Heading size="md">Appointment Summary</Heading>
            <Separator />
            <HStack justify="space-between">
              <Text fontWeight="bold">Patient:</Text>
              <Text>{userInfo.name}</Text>
            </HStack>
            <HStack justify="space-between">
              <Text fontWeight="bold">Hospital:</Text>
              <Text>{hospital?.name}</Text>
            </HStack>
            <HStack justify="space-between">
              <Text fontWeight="bold">Doctor:</Text>
              <Text>{doctor?.name}</Text>
            </HStack>
            <HStack justify="space-between">
              <Text fontWeight="bold">Specialty:</Text>
              <Text>{doctor?.specialty}</Text>
            </HStack>
            <HStack justify="space-between">
              <Text fontWeight="bold">Time:</Text>
              <Text>{selectedTime}</Text>
            </HStack>
            <HStack justify="space-between">
              <Text fontWeight="bold">Phone:</Text>
              <Text>{userInfo.phone}</Text>
            </HStack>
          </Stack>
        </Box>
        {error && (
          <Alert.Root status="error">
            <Alert.Indicator />
            <Alert.Title>{error}</Alert.Title>
          </Alert.Root>
        )}
        <HStack gap={4}>
          <Button variant="outline" onClick={() => setCurrentStep(4)} flex={1}>
            Back to Time Selection
          </Button>
          <Button
            colorScheme="green"
            onClick={handleConfirmBooking}
            loading={createAppointmentMutation.isPending}
            loadingText="Booking..."
            flex={1}
          >
            Confirm Appointment
          </Button>
        </HStack>
      </Stack>
    )
  }

  const renderCurrentStep = () => {
    switch (currentStep) {
      case 1:
        return renderStep1()
      case 2:
        return renderStep2()
      case 3:
        return renderStep3()
      case 4:
        return renderStep4()
      case 5:
        return renderStep5()
      default:
        return renderStep1()
    }
  }

  return (
    <Container maxW="4xl" py={8}>
      <Stack gap={8} align="stretch">
        <Heading textAlign="center">
          Medical Appointment Booking Service
        </Heading>

        {/* Progress indicator */}
        <HStack justify="center" gap={4}>
          {[1, 2, 3, 4, 5].map((step) => (
            <Badge
              key={step}
              colorScheme={currentStep >= step ? "blue" : "gray"}
              fontSize="sm"
              px={3}
              py={1}
            >
              Step {step}
            </Badge>
          ))}
        </HStack>

        {renderCurrentStep()}
      </Stack>
    </Container>
  )
}

/**
 * 
 * 页面功能描述
step 1：输入用户身份信息，点击提交
- 成功：后台自动校验，跳转医院选择界面
- 失败：提示用户校验失败，重新输入身份信息
step 2：选择医院
- 成功：后台自动校验，跳转医生选择界面
- 失败：提示用户校验失败，重新输入医院信息
step 3：选择医生
- 成功：后台自动校验，跳转可预约时间界面
- 失败：提示用户校验失败，重新输入医生信息
step 4：查看所选医生的可预约时间
- 有想预约的时间：选择预约时间
- 没有想预约的时间：返回医院选择界面重新选择
step 5：系统确认预约，发送预约成功的消息
- 成功：提示用户预约成功
- 失败：提示用户预约失败
 * 
 */
