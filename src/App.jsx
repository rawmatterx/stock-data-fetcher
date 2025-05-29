import React, { useState } from 'react';
import { ChakraProvider, Box, VStack, Container, Heading } from '@chakra-ui/react';
import StockDataForm from './components/StockDataForm';
import StockDataDisplay from './components/StockDataDisplay';
import { QueryClient, QueryClientProvider } from 'react-query';

const queryClient = new QueryClient();

function App() {
  const [stockData, setStockData] = useState(null);

  return (
    <QueryClientProvider client={queryClient}>
      <ChakraProvider>
        <Box minH="100vh" bg="gray.50" py={8}>
          <Container maxW="container.xl">
            <VStack spacing={8}>
              <Heading as="h1" size="xl" color="blue.600">
                📈 Stock Data Analyzer
              </Heading>
              <StockDataForm onDataFetched={setStockData} />
              {stockData && <StockDataDisplay data={stockData} />}
            </VStack>
          </Container>
        </Box>
      </ChakraProvider>
    </QueryClientProvider>
  );
}

export default App