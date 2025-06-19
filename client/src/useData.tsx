import useSWR from "swr";

const fetcher = (...args) => fetch(...args).then((res) => res.json());

export function useData() {
  const { data, error, isLoading } = useSWR(
    `http://${window.location.hostname}:8000/data`,
    fetcher
  );

  return { data, error, isLoading };
}
