import useSWR from "swr";

const fetcher = (...args: Parameters<typeof fetch>) =>
  fetch(...args).then((res) => res.json());

interface UseDataParams {
  startDate?: Date | null;
  endDate?: Date | null;
}

interface SystemStats {
  cpu_usage: number;
  memory_usage: number;
  disk_usage: number;
  uptime: number;
  fan_rpm: number;
  cpu_temperature: number;
}

interface Settings {
  AS7341: {
    enabled: boolean;
    i2c_bus: number;
    i2c_address: number;
    sample_interval: number;
  };
  BME688: {
    enabled: boolean;
    i2c_bus: number;
    i2c_address: number;
    sea_level_pressure: number;
    sample_interval: number;
  };
  ENS160: {
    enabled: boolean;
    i2c_bus: number;
    i2c_address: number;
    sample_interval: number;
  };
  LTR390: {
    enabled: boolean;
    i2c_bus: number;
    i2c_address: number;
    sample_interval: number;
  };
  SPS30: {
    enabled: boolean;
    i2c_bus: number;
    i2c_address: number;
    sample_interval: number;
  };
  timelapse: {
    enabled: boolean;
    interval: number;
  };
}

export function useSensorData({ startDate, endDate }: UseDataParams) {
  // Build URL with query parameters
  let url = `http://${window.location.hostname}:8000/sensors/data`;
  const params = new URLSearchParams();

  if (startDate) params.append("start_date", startDate.toISOString());
  if (endDate) params.append("end_date", endDate.toISOString());

  if (params.toString()) url += `?${params.toString()}`;

  const { data, error, isLoading } = useSWR(url, fetcher);
  return { data, error, isLoading };
}

export function useSystemStats() {
  const url = `http://${window.location.hostname}:8000/system/stats`;
  const { data, error, isLoading } = useSWR<SystemStats>(url, fetcher, {
    refreshInterval: 5000, // Refresh every 5 seconds
  });
  return { data, error, isLoading };
}

export function useSettings() {
  const url = `http://${window.location.hostname}:8000/settings`;
  const { data, error, isLoading } = useSWR<Settings>(url, fetcher, {
    refreshInterval: 5000, // Refresh every 5 seconds
  });
  return { data, error, isLoading };
}
