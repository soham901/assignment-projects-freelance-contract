import { connectDB, Lead } from "./src/db.js";

import express from 'express';


const app = express();

console.log("SERVER STARTED");

connectDB();

app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(express.static('public'));


// TODO: Seperate routes into their own files
app.get('/leads', async (req, res) => {
    try {
        const leads = await Lead.find();
        res.send(leads);
    }
    catch (error) {
        res.status(500).json({ error: error.message });
    }
});


app.put('/leads', async (req, res) => {
    try {
        const { id, first_name, last_name, phone_work } = req.body;

        if (!id) {
            return res.status(400).json({ message: 'ID is required' });
        }

        const lead = await Lead.findOne({ id });

        if (!lead) {
            return res.status(404).json({ message: 'Lead not found' });
        }

        // TODO: Add validation
        lead.first_name = first_name || lead.first_name;
        lead.last_name = last_name || lead.last_name;
        lead.phone_work = phone_work || lead.phone_work;

        await lead.save();

        res.send(lead);
    }

    catch (error) {
        res.status(500).json({ error: error.message });
    }
});



app.delete('/leads', async (req, res) => {
    try {

        console.log('req.body', req.body);

        const { id } = req.body;

        console.log('id', id);

        if (!id) {
            return res.status(400).json({ message: 'ID is required' });
        }

        const lead = await Lead.findOneAndDelete({ id });

        console.log('lead', lead);

        if (!lead) {
            return res.status(404).json({ message: 'Lead not found' });
        }

        // const lead = await Lead.findOne({ id: req.params.id });

        // if (!lead) {
        //     return res.status(404).json({ message: 'Lead not found' });
        // }

        // await lead.remove();

        res.json({ message: 'Lead removed' });
    }

    catch (error) {
        res.status(500).json({ error: error.message });
    }
});


const PORT = process.env.PORT || 5000;

app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
