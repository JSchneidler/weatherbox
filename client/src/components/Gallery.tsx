import { Image, Text, Pagination, Grid, Group } from "@mantine/core";
import { useState } from "react";

import { useImages } from "../hooks";

function Gallery({ startDate, endDate }: { startDate?: Date; endDate?: Date }) {
  const [page, setPage] = useState(1);

  const { data, error, isLoading } = useImages({
    startDate,
    endDate,
    page,
    limit: 12,
  });

  if (isLoading) return <Text>Loading...</Text>;
  if (error) return <Text>Error: {error.message}</Text>;

  return (
    <>
      <Grid gutter="xs">
        {data?.images.map((image) => (
          <Grid.Col span={1} key={image.id}>
            <Image
              src={`http://${window.location.hostname}:8000/images/${image.id}/thumbnail`}
              h={150}
              w="auto"
              alt={image.filename}
            />
          </Grid.Col>
        ))}
      </Grid>
      <Group justify="center">
        <Pagination
          total={data?.total_pages || 1}
          value={page}
          mt="md"
          onChange={setPage}
        />
      </Group>
    </>
  );
}

export default Gallery;
