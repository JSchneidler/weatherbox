import { Image, Text, Pagination, Grid, Group, Modal } from "@mantine/core";
import { useState } from "react";

import { useImages } from "../hooks";

interface Image {
  id: string;
  filename: string;
}

function Gallery({ startDate, endDate }: { startDate?: Date; endDate?: Date }) {
  const [page, setPage] = useState(1);
  const [image, setImage] = useState<Image | null>(null);

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
      <Modal
        opened={!!image}
        onClose={() => setImage(null)}
        title={image?.filename}
        fullScreen
      >
        <Image
          src={`http://${window.location.hostname}:8000/images/${image?.id}?size=large`}
          alt={image?.filename}
        />
      </Modal>

      <Grid gutter="xs">
        {data?.images.map((image) => (
          <Grid.Col span={1} key={image.id}>
            <Image
              style={{ cursor: "pointer" }}
              src={`http://${window.location.hostname}:8000/images/${image.id}`}
              h={150}
              w="auto"
              alt={image.filename}
              onClick={() => setImage(image)}
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
