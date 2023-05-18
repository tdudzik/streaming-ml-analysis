import React, { useEffect, useState } from 'react';
import { useForm, Controller } from 'react-hook-form';
import {
    Table, TableBody, TableCell, TableHead, TableRow, Button, FormControl, InputLabel, Select, MenuItem,
    Dialog, DialogActions, DialogContent, DialogContentText, DialogTitle,
    TextField, Box, Alert, Typography, Card, CardActions, CardContent
} from '@mui/material';
import Grid from '@mui/material/Grid';
import Paper from '@mui/material/Paper';
import Title from './Title';

export default function Trainings() {
    const { control, register, handleSubmit, reset } = useForm();
    const [trainings, setTrainings] = useState([]);
    const [open, setOpen] = useState(false);
    const [datasets, setDatasets] = useState([]);
    const [selectedDatasetId, setSelectedDatasetId] = useState('');
    const [schedule, setSchedule] = useState(null);
    const [openSchedule, setOpenSchedule] = useState(false);

    const handleClickOpen = () => {
        setOpen(true);
    };

    const handleClose = () => {
        setOpen(false);
        setSelectedDatasetId('');
    };

    const onSubmit = (data) => {
        fetch('http://localhost:8083/trainings', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
            .then(response => response.json())
            .then(data => {
                setTrainings([...trainings, data]);
                handleClose();
                reset();
            })
            .catch(error => console.error('Error:', error));
    };

    const handleScheduleOpen = () => {
        setOpenSchedule(true);
    };

    const handleScheduleClose = () => {
        setOpenSchedule(false);
    };

    const onSubmitSchedule = (data) => {
        fetch('http://localhost:8083/trainings/schedule', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
            .then(response => response.json())
            .then(data => {
                setSchedule(data);
                handleScheduleClose();
                reset();
            })
            .catch(error => console.error('Error:', error));
    };

    const onScheduleCancel = () => {
        fetch('http://localhost:8083/trainings/schedule', {
            method: 'DELETE'
        })
            .then(response => {
                if (!response.ok) { throw response }
                return response.json();
            })
            .then(data => {
                setSchedule(null);
                console.log("Schedule cancelled successfully");
            })
            .catch(error => console.error('Error:', error));
    };

    useEffect(() => {
        fetch('http://localhost:8082/datasets')
            .then(response => response.json())
            .then(data => setDatasets(data))
            .catch(error => console.error('Error:', error));
    }, []);

    useEffect(() => {
        fetch('http://localhost:8083/trainings')
            .then(response => response.json())
            .then(data => setTrainings(data))
            .catch(error => console.error('Error:', error));
    }, []);

    useEffect(() => {
        fetch('http://localhost:8083/trainings/schedule')
            .then(response => {
                if (!response.ok) { throw response }
                return response.json();  //we only proceed to the next .then if the status was ok.
            })
            .then(data => setSchedule(data))
            .catch(error => {
                setSchedule(null);
                console.log(error);
            });
    }, []);

    const [currentTime, setCurrentTime] = useState(getFormattedTime());

    function getFormattedTime() {
        const now = new Date();
        return now.toISOString().substring(0, 19).replace('T', ' ');
    };

    useEffect(() => {
        const timerID = setInterval(() => {
            setCurrentTime(getFormattedTime());
        }, 1000);

        return function cleanup() {
            clearInterval(timerID);
        };
    }, []);;

    const renderMetricsTable = (metrics) => {
        const keys = Object.keys(metrics);
        return (
            <Table size="small">
                <TableHead>
                    <TableRow>
                        <TableCell>Metryka</TableCell>
                        <TableCell>Wartość</TableCell>
                    </TableRow>
                </TableHead>
                <TableBody>
                    {keys.map(key => (
                        <TableRow key={key}>
                            <TableCell>{key}</TableCell>
                            <TableCell>{JSON.stringify(metrics[key])}</TableCell>
                        </TableRow>
                    ))}
                </TableBody>
            </Table>
        );
    };

    const [metrics, setMetrics] = useState(null);
    const [openMetrics, setOpenMetrics] = useState(false);

    const handleMetricsOpen = (metrics) => {
        setMetrics(metrics);
        setOpenMetrics(true);
    };

    const handleMetricsClose = () => {
        setOpenMetrics(false);
    };

    return (
        <React.Fragment>
            <Grid item xs={12}>
                <Paper sx={{ p: 2, display: 'flex', flexDirection: 'column' }}>
                    <Title>Training Schedule</Title>
                    {schedule ? (
                        <Card sx={{ mt: 3 }}>
                            <CardContent>
                                <Typography color="text.secondary" gutterBottom>
                                    Current training schedule:
                                </Typography>
                                <Typography variant="h5" component="div">
                                    Every {schedule.interval} {schedule.intervalUnit}
                                </Typography>
                                <Typography color="text.secondary">
                                    Created at: {schedule.createdAt}
                                </Typography>
                                <Typography color="text.secondary">
                                    Current time: {currentTime}
                                </Typography>
                            </CardContent>
                            <CardActions>
                                <Button size="small" onClick={onScheduleCancel}>Cancel</Button>
                            </CardActions>
                        </Card>
                    ) : (
                        <Alert severity="info">No training schedule found.</Alert>
                    )}
                </Paper>
            </Grid>

            <Grid item xs={12}>
                <Paper sx={{ p: 2, display: 'flex', flexDirection: 'column' }}>
                    <Title>Trainings</Title>
                    <Box sx={{ display: 'flex', justifyContent: 'flex-end', m: 1 }}>
                        <Button variant="outlined" color="primary" onClick={handleClickOpen} size="small">
                            Add Training
                        </Button>
                        <Button variant="outlined" color="primary" onClick={handleScheduleOpen} size="small">
                            {schedule ? 'Update Schedule' : 'Add Schedule'}
                        </Button>
                    </Box>
                    <Dialog open={open} onClose={handleClose} aria-labelledby="form-dialog-title">
                        <DialogTitle id="form-dialog-title">Add Training</DialogTitle>
                        <DialogContent>
                            <DialogContentText>
                                To add a training, please select a dataset.
                            </DialogContentText>
                            <form onSubmit={handleSubmit(onSubmit)}>
                                <FormControl fullWidth sx={{ mt: 2 }}>
                                    <InputLabel id="dataset-select-label">Dataset</InputLabel>
                                    <Controller
                                        name="datasetId"
                                        control={control}
                                        defaultValue=""
                                        render={({ field }) => (
                                            <Select
                                                labelId="dataset-select-label"
                                                id="dataset-select"
                                                value={field.value}
                                                label="Dataset"
                                                onChange={field.onChange}
                                            >
                                                {datasets.map((dataset) => (
                                                    <MenuItem key={dataset.datasetId} value={dataset.datasetId}>
                                                        {dataset.name}
                                                    </MenuItem>
                                                ))}
                                            </Select>
                                        )}
                                    />
                                </FormControl>
                                <DialogActions>
                                    <Button onClick={handleClose} color="primary">
                                        Cancel
                                    </Button>
                                    <Button type="submit" color="primary">
                                        Add
                                    </Button>
                                </DialogActions>
                            </form>
                        </DialogContent>
                    </Dialog>
                    <Dialog open={openSchedule} onClose={handleScheduleClose} aria-labelledby="form-dialog-title-schedule">
                        <DialogTitle id="form-dialog-title-schedule">Schedule Training</DialogTitle>
                        <DialogContent>
                            <DialogContentText>
                                To schedule a training, please provide the interval and unit.
                            </DialogContentText>
                            <form onSubmit={handleSubmit(onSubmitSchedule)}>
                                <FormControl fullWidth sx={{ mt: 2 }}>
                                    <Controller
                                        name="interval"
                                        control={control}
                                        defaultValue=""
                                        render={({ field }) => (
                                            <TextField
                                                {...field}
                                                label="Interval"
                                                type="number"
                                            />
                                        )}
                                    />
                                    <Controller
                                        name="interval_unit"
                                        control={control}
                                        defaultValue=""
                                        render={({ field }) => (
                                            <Select
                                                labelId="interval-unit-select-label"
                                                id="interval-unit-select"
                                                value={field.value}
                                                label="Interval Unit"
                                                onChange={field.onChange}
                                            >
                                                <MenuItem value="minutes">Minutes</MenuItem>
                                                <MenuItem value="hours">Hours</MenuItem>
                                                <MenuItem value="days">Days</MenuItem>
                                            </Select>
                                        )}
                                    />
                                </FormControl>
                                <DialogActions>
                                    <Button onClick={handleScheduleClose} color="primary">
                                        Cancel
                                    </Button>
                                    <Button type="submit" color="primary">
                                        Schedule
                                    </Button>
                                </DialogActions>
                            </form>
                        </DialogContent>
                    </Dialog>
                    <Box sx={{ m: 3 }}>
                        <Table size="small">
                            <TableHead>
                                <TableRow>
                                    <TableCell>Dataset ID</TableCell>
                                    <TableCell>Dataset name</TableCell>
                                    <TableCell>Status</TableCell>
                                    <TableCell>Created at</TableCell>
                                    <TableCell>Completed at</TableCell>
                                    <TableCell>Metrics</TableCell> {/* Keep this column */}
                                </TableRow>
                            </TableHead>
                            <TableBody>
                                {trainings.map((training) => (
                                    <TableRow key={training.trainingId}>
                                        <TableCell>{training.datasetId}</TableCell>
                                        <TableCell>{training.datasetName}</TableCell>
                                        <TableCell>{training.status}</TableCell>
                                        <TableCell>{training.createdAt}</TableCell>
                                        <TableCell>{(training.completedAt && training.completedAt) || "-"}</TableCell>
                                        <TableCell>
                                            <Button
                                                size="small"
                                                variant="outlined"
                                                color="primary"
                                                onClick={() => handleMetricsOpen(training.metrics)}
                                                disabled={!training.metrics}
                                            >
                                                View Metrics
                                            </Button>
                                        </TableCell>
                                    </TableRow>
                                ))}
                            </TableBody>
                        </Table>
                    </Box>

                    <Dialog open={openMetrics} onClose={handleMetricsClose} aria-labelledby="metrics-dialog-title">
                        <DialogTitle id="metrics-dialog-title">Metrics</DialogTitle>
                        <DialogContent>
                            {metrics ? renderMetricsTable(metrics) : "No metrics available"}
                        </DialogContent>
                        <DialogActions>
                            <Button onClick={handleMetricsClose} color="primary">
                                Close
                            </Button>
                        </DialogActions>
                    </Dialog>
                </Paper>
            </Grid>
        </React.Fragment>
    );
}
