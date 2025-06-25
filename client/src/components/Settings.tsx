import {
  Group,
  LoadingOverlay,
  NumberInput,
  Select,
  Stack,
  Switch,
  Title,
  Divider,
  TextInput,
} from "@mantine/core";

import { useSettings } from "../hooks";

const I2CBusDropdown = ({ value }: { value: number | undefined }) => {
  return (
    <Select
      disabled
      label="I2C Bus"
      data={["0", "1"]}
      value={value?.toString()}
    />
  );
};

const Settings = () => {
  const {
    data: settings,
    error: settingsError,
    isLoading: settingsLoading,
  } = useSettings();

  if (settingsLoading) {
    return <LoadingOverlay visible={true} />;
  }

  if (settingsError) {
    return <div>Error: {settingsError.message}</div>;
  }

  return (
    <Stack>
      <Stack>
        <Group>
          <Title order={4}>Timelapse</Title>
          <Switch disabled checked={settings?.timelapse.enabled} />
        </Group>
        <Group>
          <NumberInput
            disabled
            label="Timelapse Interval"
            value={settings?.timelapse.interval}
          />
        </Group>
      </Stack>

      <Divider />

      <Stack>
        <Group>
          <Title order={4}>AS7341</Title>
          <Switch disabled checked={settings?.AS7341.enabled} />
        </Group>
        <Group>
          <I2CBusDropdown value={settings?.AS7341.i2c_bus} />
          <TextInput
            disabled
            label="I2C Address"
            value={settings?.AS7341.i2c_address}
          />
          <NumberInput
            disabled
            label="Sample Interval"
            value={settings?.AS7341.sample_interval}
          />
        </Group>
      </Stack>

      <Divider />

      <Stack>
        <Group>
          <Title order={4}>BME688</Title>
          <Switch disabled checked={settings?.BME688.enabled} />
        </Group>
        <Group>
          <I2CBusDropdown value={settings?.BME688.i2c_bus} />
          <TextInput
            disabled
            label="I2C Address"
            value={settings?.BME688.i2c_address}
          />
          <NumberInput
            disabled
            label="Sample Interval"
            value={settings?.BME688.sample_interval}
          />
          <NumberInput
            disabled
            label="Sea Level Pressure"
            value={settings?.BME688.sea_level_pressure}
          />
        </Group>
      </Stack>

      <Divider />

      <Stack>
        <Group>
          <Title order={4}>ENS160</Title>
          <Switch disabled checked={settings?.ENS160.enabled} />
        </Group>
        <Group>
          <I2CBusDropdown value={settings?.ENS160.i2c_bus} />
          <TextInput
            disabled
            label="I2C Address"
            value={settings?.ENS160.i2c_address}
          />
          <NumberInput
            disabled
            label="Sample Interval"
            value={settings?.ENS160.sample_interval}
          />
        </Group>
      </Stack>

      <Divider />

      <Stack>
        <Group>
          <Title order={4}>LTR390</Title>
          <Switch disabled checked={settings?.LTR390.enabled} />
        </Group>
        <Group>
          <I2CBusDropdown value={settings?.LTR390.i2c_bus} />
          <TextInput
            disabled
            label="I2C Address"
            value={settings?.LTR390.i2c_address}
          />
          <NumberInput
            disabled
            label="Sample Interval"
            value={settings?.LTR390.sample_interval}
          />
        </Group>
      </Stack>

      <Divider />

      <Stack>
        <Group>
          <Title order={4}>SPS30</Title>
          <Switch disabled checked={settings?.SPS30.enabled} />
        </Group>
        <Group>
          <I2CBusDropdown value={settings?.SPS30.i2c_bus} />
          <TextInput
            disabled
            label="I2C Address"
            value={settings?.SPS30.i2c_address}
          />
          <NumberInput
            disabled
            label="Sample Interval"
            value={settings?.SPS30.sample_interval}
          />
        </Group>
      </Stack>
    </Stack>
  );
};

export default Settings;
