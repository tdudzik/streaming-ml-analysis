import React, { useEffect, useState, useRef } from 'react';
import { useForm } from 'react-hook-form';
import {
    Table, TableBody, TableCell, TableHead, TableRow, Button, Typography,
    Dialog, DialogActions, DialogContent, DialogContentText, DialogTitle,
    TextField, Box
} from '@mui/material';
import Grid from '@mui/material/Grid';
import Paper from '@mui/material/Paper';
import Title from './Title';

export default function Datasets() {
    const { register, handleSubmit, reset } = useForm();
    const [datasets, setDatasets] = useState([]);
    const [open, setOpen] = useState(false);
    const [selectedFile, setSelectedFile] = useState(null);
    const [selectedFileName, setSelectedFileName] = useState('');

    const fileInputRef = useRef(null);

    const handleClickOpen = () => {
        setOpen(true);
    };

    const handleClose = () => {
        setOpen(false);
        setSelectedFile(null);
        setSelectedFileName('');
    };

    const onFileChange = (event) => {
        const file = event.target.files[0];
        setSelectedFile(file);
        setSelectedFileName(file ? file.name : '');
    };

    const onSubmit = (data) => {
        const formData = new FormData();
        formData.append('name', data.name);
        if (selectedFile) {
            formData.append('file', selectedFile);
        }
        fetch('http://localhost:8082/datasets', {
            method: 'POST',
            body: formData
        })
            .then(response => response.json())
            .then(data => {
                setDatasets([...datasets, data]);
                handleClose();
                reset();
            })
            .catch(error => console.error('Error:', error));
    };

    useEffect(() => {
        fetch('http://localhost:8082/datasets')
            .then(response => response.json())
            .then(data => setDatasets(data))
            .catch(error => console.error('Error:', error));
    }, []);

    return (
        <Grid item xs={12}>
            <Paper sx={{ p: 2, display: 'flex', flexDirection: 'column' }}>
                <Title>Datasets</Title>
                <Box sx={{ display: 'flex', justifyContent: 'flex-end', m: 1 }}>
                    <Button variant="outlined" color="primary" onClick={handleClickOpen} size="small">
                        Add Dataset
                    </Button>
                </Box>
                <Dialog open={open} onClose={handleClose} aria-labelledby="form-dialog-title">
                    <DialogTitle id="form-dialog-title">Add Dataset</DialogTitle>
                    <DialogContent>
                        <DialogContentText>
                            To add a dataset, please enter the dataset name and upload a file.
                        </DialogContentText>
                        <form onSubmit={handleSubmit(onSubmit)}>
                            <TextField
                                autoFocus
                                margin="dense"
                                id="name"
                                label="Dataset Name"
                                type="text"
                                fullWidth
                                {...register('name')}
                            />
                            <Box sx={{ display: 'flex', alignItems: 'center', mt: 2 }}>
                                <label htmlFor="contained-button-file">
                                    <Button variant="contained" component="span">
                                        Select File
                                    </Button>
                                </label>
                                <input
                                    accept="*/*"
                                    style={{ display: 'none' }}
                                    id="contained-button-file"
                                    type="file"
                                    onChange={onFileChange}
                                    ref={fileInputRef}
                                />
                                {selectedFileName && (
                                    <Box sx={{ ml: 2 }}>
                                        <Typography variant="body2" sx={{ fontSize: '0.8rem' }}>
                                            {selectedFileName}
                                        </Typography>
                                    </Box>
                                )}
                            </Box>
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
                <Box sx={{ m: 3 }}>
                    <Table size="small">
                        <TableHead>
                            <TableRow>
                                <TableCell>Dataset ID</TableCell>
                                <TableCell>Name</TableCell>
                                <TableCell>URI</TableCell>
                                <TableCell>Created At</TableCell>
                            </TableRow>
                        </TableHead>
                        <TableBody>
                            {datasets.map((dataset) => (
                                <TableRow key={dataset.datasetId}>
                                    <TableCell>{dataset.datasetId}</TableCell>
                                    <TableCell>{dataset.name}</TableCell>
                                    <TableCell>{dataset.uri}</TableCell>
                                    <TableCell>{dataset.createdAt}</TableCell>
                                </TableRow>
                            ))}
                        </TableBody>
                    </Table>
                </Box>
            </Paper>
        </Grid>
    );
}
