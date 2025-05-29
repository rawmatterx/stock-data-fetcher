import React, { useState } from 'react';
import {
  Box,
  Button,
  FormControl,
  FormLabel,
  Input,
  VStack,
  useToast,
  Text,
  Textarea,
  HStack,
} from '@chakra-ui/react';
import { useMutation } from 'react-query';
import { format } from 'date-fns';

const StockDataForm = ({ onDataFetched }) => {
  const [symbols, setSymbols] = useState('');
  const [startDate, setStartDate] = useState(
    format(new Date(Date.now() - 365 * 24 * 60 * 60 * 1000), 'yyyy-MM-dd')
  );
  const [endDate, setEndDate] = useState(format(new Date(), 'yyyy-MM-dd'));
  const toast = useToast();

  const fetchStockData = async (formData) => {
    // This is where we'd normally make an API call
    // For now, we'll simulate the API response
    const symbolList = formData.symbols.split('\n').map(s => s.trim()).filter(Boolean);
    
    // Simulate API delay
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    // Mock data structure
    return {
      data: symbolList.map(symbol => ({
        symbol,
        dates: [...Array(10)].map((_, i) => ({
          date: new Date(Date.now() - i * 24 * 60 * 60 * 1000),
          close: Math.random() * 1000,
          volume: Math.floor(Math.random() * 1000000)
        }))
      }))
    };
  };

  const mutation = useMutation(fetchStockData, {
    onSuccess: (data) => {
      onDataFetched(data);
      toast({
        title: 'Data fetched successfully',
        status: 'success',
        duration: 3000,
        isClosable: true,
      });
    },
    onError: (error) => {
      toast({
        title: 'Error fetching data',
        description: error.message,
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
    },
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    mutation.mutate({ symbols, startDate, endDate });
  };

  return (
    <Box w="100%" bg="white" p={6} borderRadius="lg" boxShadow="md">
      <form onSubmit={handleSubmit}>
        <VStack spacing={4}>
          <FormControl isRequired>
            <FormLabel>Stock Symbols (one per line)</FormLabel>
            <Textarea
              value={symbols}
              onChange={(e) => setSymbols(e.target.value)}
              placeholder="Enter stock symbols..."
              rows={5}
            />
          </FormControl>
          
          <HStack w="100%" spacing={4}>
            <FormControl isRequired>
              <FormLabel>Start Date</FormLabel>
              <Input
                type="date"
                value={startDate}
                onChange={(e) => setStartDate(e.target.value)}
              />
            </FormControl>
            
            <FormControl isRequired>
              <FormLabel>End Date</FormLabel>
              <Input
                type="date"
                value={endDate}
                onChange={(e) => setEndDate(e.target.value)}
              />
            </FormControl>
          </HStack>

          <Button
            type="submit"
            colorScheme="blue"
            isLoading={mutation.isLoading}
            w="100%"
          >
            Fetch Stock Data
          </Button>
        </VStack>
      </form>
    </Box>
  );
};

export default StockDataForm;