import {
  Stack,
  Group,
  Text,
  Badge,
  Grid,
  Paper,
  Title,
  Progress,
} from "@mantine/core";
import { useSystemStats } from "../hooks";

const formatUptime = (bootTime: number) => {
  const now = Date.now() / 1000;
  const uptimeSeconds = now - bootTime;
  const days = Math.floor(uptimeSeconds / 86400);
  const hours = Math.floor((uptimeSeconds % 86400) / 3600);
  const minutes = Math.floor((uptimeSeconds % 3600) / 60);

  if (days > 0) {
    return `${days}d ${hours}h ${minutes}m`;
  } else if (hours > 0) {
    return `${hours}h ${minutes}m`;
  } else {
    return `${minutes}m`;
  }
};

const SystemHealth = () => {
  const {
    data: systemStats,
    error: systemError,
    isLoading: systemLoading,
  } = useSystemStats();

  return (
    <Paper p="md" withBorder mt="md">
      <Stack gap="md">
        <Title order={4}>System Status</Title>
        {systemLoading ? (
          <Text size="sm" c="dimmed">
            Loading system stats...
          </Text>
        ) : systemStats ? (
          <Grid gutter="lg">
            {/* Performance Metrics */}
            <Grid.Col span={6}>
              <Stack gap="xs">
                <Stack gap="xs">
                  <Group justify="space-between">
                    <Text size="sm">CPU</Text>
                    <Badge
                      variant="light"
                      color={
                        systemStats.cpu_usage > 80
                          ? "red"
                          : systemStats.cpu_usage > 60
                          ? "yellow"
                          : "green"
                      }
                    >
                      {systemStats.cpu_usage.toFixed(1)}%
                    </Badge>
                  </Group>
                  <Progress
                    value={systemStats.cpu_usage}
                    color={
                      systemStats.cpu_usage > 80
                        ? "red"
                        : systemStats.cpu_usage > 60
                        ? "yellow"
                        : "green"
                    }
                    size="xs"
                  />
                </Stack>

                <Stack gap="xs">
                  <Group justify="space-between">
                    <Text size="sm">Memory</Text>
                    <Badge
                      variant="light"
                      color={
                        systemStats.memory_usage > 80
                          ? "red"
                          : systemStats.memory_usage > 60
                          ? "yellow"
                          : "green"
                      }
                    >
                      {systemStats.memory_usage.toFixed(1)}%
                    </Badge>
                  </Group>
                  <Progress
                    value={systemStats.memory_usage}
                    color={
                      systemStats.memory_usage > 80
                        ? "red"
                        : systemStats.memory_usage > 60
                        ? "yellow"
                        : "green"
                    }
                    size="xs"
                  />
                </Stack>

                <Stack gap="xs">
                  <Group justify="space-between">
                    <Text size="sm">Disk</Text>
                    <Badge
                      variant="light"
                      color={
                        systemStats.disk_usage > 80
                          ? "red"
                          : systemStats.disk_usage > 60
                          ? "yellow"
                          : "green"
                      }
                    >
                      {systemStats.disk_usage.toFixed(1)}%
                    </Badge>
                  </Group>
                  <Progress
                    value={systemStats.disk_usage}
                    color={
                      systemStats.disk_usage > 80
                        ? "red"
                        : systemStats.disk_usage > 60
                        ? "yellow"
                        : "green"
                    }
                    size="xs"
                  />
                </Stack>
              </Stack>
            </Grid.Col>

            {/* System Health */}
            <Grid.Col span={6}>
              <Stack gap="xs">
                <Group justify="space-between">
                  <Text size="sm">CPU Temperature</Text>
                  <Badge
                    variant="light"
                    color={
                      systemStats.cpu_temperature > 80
                        ? "red"
                        : systemStats.cpu_temperature > 60
                        ? "yellow"
                        : "green"
                    }
                  >
                    {systemStats.cpu_temperature.toFixed(1)}°C
                  </Badge>
                </Group>

                <Group justify="space-between">
                  <Text size="sm">Fan Speed</Text>
                  <Badge variant="light" color="blue">
                    {systemStats.fan_rpm.toLocaleString()} RPM
                  </Badge>
                </Group>

                <Group justify="space-between">
                  <Text size="sm">Uptime</Text>
                  <Badge variant="light" color="blue">
                    {formatUptime(systemStats.uptime)}
                  </Badge>
                </Group>

                <Group justify="space-between">
                  <Text size="sm">Fan Speed</Text>
                  <Badge variant="light" color="blue">
                    {systemStats.fan_rpm.toLocaleString()} RPM
                  </Badge>
                </Group>

                <Group justify="space-between">
                  <Text size="sm">Uptime</Text>
                  <Badge variant="light" color="blue">
                    {formatUptime(systemStats.uptime)}
                  </Badge>
                </Group>
              </Stack>
            </Grid.Col>
          </Grid>
        ) : systemError ? (
          <Text c="red" size="sm">
            Error loading system stats: {systemError.message || "Unknown error"}
          </Text>
        ) : null}
      </Stack>
    </Paper>
  );
};

export default SystemHealth;
