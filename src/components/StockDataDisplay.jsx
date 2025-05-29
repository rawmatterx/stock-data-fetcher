import React from 'react';
import {
  Box,
  VStack,
  Heading,
  Table,
  Thead,
  Tbody,
  Tr,
  Th,
  Td,
  Button,
} from '@chakra-ui/react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';
import { format } from 'date-fns';

const StockDataDisplay = ({ data }) => {
  const downloadCsv = () => {
    // Implementation for CSV download
    const csvContent = 'data:text/csv;charset=utf-8,' + 
      'Symbol,Date,Close,Volume\n' +
      data.data.map(stock => 
        stock.dates.map(date => 
          `${stock.symbol},${format(new Date(date.date), 'yyyy-MM-dd')},${date.close},${date.volume}`
        ).join('\n')
      ).join('\n');

    const encodedUri = encodeURI(csvContent);
    const link = document.createElement('a');
    link.setAttribute('href', encodedUri);
    link.setAttribute('download', `stock_data_${format(new Date(), 'yyyyMMdd')}.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <VStack w="100%" spacing={6}>
      <Box w="100%" bg="white" p={6} borderRadius="lg" boxShadow="md">
        <Heading size="md" mb={4}>Stock Price Chart</Heading>
        <Box h="400px">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis
                dataKey="date"
                type="number"
                domain={['dataMin', 'dataMax']}
                tickFormatter={(unixTime) => format(new Date(unixTime), 'MM/dd')}
              />
              <YAxis />
              <Tooltip
                labelFormatter={(value) => format(new Date(value), 'yyyy-MM-dd')}
              />
              <Legend />
              {data.data.map((stock, index) => (
                <Line
                  key={stock.symbol}
                  data={stock.dates}
                  type="monotone"
                  dataKey="close"
                  name={stock.symbol}
                  stroke={`hsl(${index * 137.508}, 70%, 50%)`}
                  dot={false}
                />
              ))}
            </LineChart>
          </ResponsiveContainer>
        </Box>
      </Box>

      <Box w="100%" bg="white" p={6} borderRadius="lg" boxShadow="md">
        <Heading size="md" mb={4}>Data Table</Heading>
        <Button colorScheme="green" mb={4} onClick={downloadCsv}>
          Download CSV
        </Button>
        <Box overflowX="auto">
          <Table variant="simple">
            <Thead>
              <Tr>
                <Th>Symbol</Th>
                <Th>Date</Th>
                <Th isNumeric>Close Price</Th>
                <Th isNumeric>Volume</Th>
              </Tr>
            </Thead>
            <Tbody>
              {data.data.map(stock =>
                stock.dates.slice(0, 5).map((date, i) => (
                  <Tr key={`${stock.symbol}-${i}`}>
                    <Td>{stock.symbol}</Td>
                    <Td>{format(new Date(date.date), 'yyyy-MM-dd')}</Td>
                    <Td isNumeric>{date.close.toFixed(2)}</Td>
                    <Td isNumeric>{date.volume.toLocaleString()}</Td>
                  </Tr>
                ))
              )}
            </Tbody>
          </Table>
        </Box>
      </Box>
    </VStack>
  );
};

export default StockDataDisplay;