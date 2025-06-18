import "./App.css";

import { MantineProvider } from "@mantine/core";
import { LineChart } from "@mantine/charts";
import { useData } from "./useData";

import "@mantine/core/styles.css";
import "@mantine/charts/styles.css";

function App() {
  const { data, error, isLoading } = useData();

  if (isLoading) return <div>Loading...</div>;
  if (error) return <div>Error: {error.message}</div>;

  const as7341Data = data.as7341.map((item) => ({
    date: item.timestamp,
    violet: item.violet,
    indigo: item.indigo,
    blue: item.blue,
    cyan: item.cyan,
    green: item.green,
    yellow: item.yellow,
    orange: item.orange,
    red: item.red,
    clear: item.clear,
    nir: item.nir,
  }));
  const as7341Series = [
    { name: "violet", color: "violet.6" },
    { name: "indigo", color: "indigo.6" },
    { name: "blue", color: "blue.6" },
    { name: "cyan", color: "cyan.6" },
    { name: "green", color: "green.6" },
    { name: "yellow", color: "yellow.6" },
    { name: "orange", color: "orange.6" },
    { name: "red", color: "red.6" },
    { name: "clear", color: "gray.6" },
    { name: "nir", color: "gray.6" },
  ];

  const ltr390Data = data.ltr390.map((item) => ({
    date: item.timestamp,
    light: item.light,
  }));
  const ltr390Series = [{ name: "light", color: "blue.6" }];

  const bme688Data = data.bme688.map((item) => ({
    date: item.timestamp,
    temperature: item.temperature,
    humidity: item.humidity,
    pressure: item.pressure,
  }));
  const bme688Series = [
    { name: "temperature", color: "blue.6" },
    { name: "humidity", color: "red.6" },
    { name: "pressure", color: "green.6", yAxisId: "right" },
  ];

  const ens160Data = data.ens160.map((item) => ({
    date: item.timestamp,
    aqi: item.aqi,
    tvoc: item.tvoc,
    eco2: item.eco2,
  }));
  const ens160Series = [
    { name: "aqi", color: "blue.6", yAxisId: "right" },
    { name: "tvoc", color: "red.6" },
    { name: "eco2", color: "green.6" },
  ];

  return (
    <MantineProvider defaultColorScheme="dark">
      <LineChart
        h={300}
        w={1000}
        data={as7341Data}
        dataKey="date"
        series={as7341Series}
        curveType="linear"
        withDots={false}
      />
      <LineChart
        h={300}
        w={1000}
        data={bme688Data}
        dataKey="date"
        series={bme688Series}
        curveType="linear"
        withDots={false}
        withRightYAxis
      />
      <LineChart
        h={300}
        w={1000}
        data={ltr390Data}
        dataKey="date"
        series={ltr390Series}
        curveType="linear"
        withDots={false}
      />
      <LineChart
        h={300}
        w={1000}
        data={ens160Data}
        dataKey="date"
        series={ens160Series}
        curveType="linear"
        withDots={false}
        withRightYAxis
      />
    </MantineProvider>
  );
}

export default App;
