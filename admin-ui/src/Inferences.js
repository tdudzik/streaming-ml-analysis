import React, { useEffect, useState } from 'react';
import {
    Table, TableBody, TableCell, TableHead, TableRow, Button,
    Dialog, DialogActions, DialogContent, DialogTitle,
    TextField, Box, Grid, Paper,
} from '@mui/material';
import Title from './Title';

export default function Inferences() {
    const [inferences, setInferences] = useState([]);
    const [openData, setOpenData] = useState(false);
    const [data, setData] = useState(null);
    const [fromTime, setFromTime] = useState(null);
    const [toTime, setToTime] = useState(null);

    const handleDataOpen = (data) => {
        setData(data);
        setOpenData(true);
    };

    const handleDataClose = () => {
        setData(null);
        setOpenData(false);
    };

    useEffect(() => {
        let url = 'http://localhost:8084/inferences';
        if (fromTime && toTime) {
            url += `?from_time=${new Date(fromTime).toISOString()}&to_time=${new Date(toTime).toISOString()}`;
        }
        fetch(url)
            .then(response => response.json())
            .then(data => setInferences(data))
            .catch(error => console.error('Error:', error));
    }, [fromTime, toTime]);

    return (
        <React.Fragment>
            <Grid item xs={12}>
                <Paper sx={{ p: 2, display: 'flex', flexDirection: 'column' }}>
                    <Title>Inferences</Title>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', m: 1 }}>
                        <TextField
                            label="From Time"
                            type="datetime-local"
                            InputLabelProps={{ shrink: true }}
                            value={fromTime}
                            onChange={(event) => setFromTime(event.target.value)}
                        />
                        <TextField
                            label="To Time"
                            type="datetime-local"
                            InputLabelProps={{ shrink: true }}
                            value={toTime}
                            onChange={(event) => setToTime(event.target.value)}
                        />
                    </Box>
                    <Box sx={{ m: 3 }}>
                        <Table size="small">
                            <TableHead>
                                <TableRow>
                                    <TableCell>Inference ID</TableCell>
                                    <TableCell>Date</TableCell>
                                    <TableCell>Name</TableCell>
                                    <TableCell>Result</TableCell>
                                    <TableCell>Show Data</TableCell>
                                </TableRow>
                            </TableHead>
                            <TableBody>
                                {inferences.map((inference) => (
                                    <TableRow key={inference.inferenceId}>
                                        <TableCell>{inference.inferenceId}</TableCell>
                                        <TableCell>{new Date(inference.createdAt).toLocaleString()}</TableCell>
                                        <TableCell>{inference.name}</TableCell>
                                        <TableCell>{inference.result ? "Successful" : "Unsuccessful"}</TableCell>
                                        <TableCell>
                                            <Button
                                                size="small"
                                                variant="outlined"
                                                color="primary"
                                                onClick={() => handleDataOpen(inference.data)}
                                                disabled={!inference.data}
                                            >
                                                Show Data
                                            </Button>
                                        </TableCell>
                                    </TableRow>
                                ))}
                            </TableBody>
                        </Table>
                    </Box>

                    <Dialog open={openData} onClose={handleDataClose} aria-labelledby="data-dialog-title">
                        <DialogTitle id="data-dialog-title">Data</DialogTitle>
                        <DialogContent>
                            <pre>
                                {data ? JSON.stringify(data, null, 2) : "No data available"}
                            </pre>
                        </DialogContent>
                        <DialogActions>
                            <Button onClick={handleDataClose} color="primary">
                                Close
                            </Button>
                        </DialogActions>
                    </Dialog>
                </Paper>
            </Grid>
        </React.Fragment>
    );
}
