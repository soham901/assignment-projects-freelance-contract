import { connectDB, Lead } from "./src/db.js";

import express from 'express';


const app = express();

connectDB();

app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(express.static('public'));


// TODO: Seperate routes into their own files
app.get('/leads', async (req, res) => {
    const leads = await Lead.find();

    // send the leads but with html table
    res.send(`
    <table border="1">
        <tr>
            <th>ID</th>
            <th>First Name</th>
            <th>Last Name</th>
            <th>Phone Work</th>
            <th>Action</th>
        </tr>
        ${leads.map(lead => `
            <tr id="lead-${lead.id}">
                <td>${lead.id}</td>
                <td>${lead.first_name}</td>
                <td>${lead.last_name}</td>
                <td>${lead.phone_work}</td>
                <td
                hx-get="/lead/${lead.id}/edit"
                hx-trigger="click"
                hx-swap="innerHTML"
                hx-target="#lead-${lead.id}"
                style="background-color: blue; color: white;"
                >
                    Edit
                </td>
            </tr>
        `).join('')}
    </table>
    `);
});


app.get('/lead/:id/edit', async (req, res) => {

    const lead = await Lead.findOne({ id: req.params.id });


    res.send(`
                <td>${lead.id}</td>
                <td contenteditable onblur="handleBlur('first_name')">${lead.first_name}</td>
                <td contenteditable onblur="handleBlur('last_name')">${lead.last_name}</td>
                <td contenteditable onblur="handleBlur('phone_work')">${lead.phone_work}</td>
                <td
                hx-get="/lead/${lead.id}/save"
                hx-trigger="click"
                hx-swap="innerHTML"
                hx-target="#lead-${lead.id}"
                style="background-color: green; color: white;"
                >
                    Save
                </td>
    `);
});


app.get('/lead/:id/save', async (req, res) => {
    const lead = await Lead.findOne({ id: req.params.id });
    console.log(lead);
    res.send(`
                <td>${lead.id}</td>
                <td>${lead.first_name}</td>
                <td>${lead.last_name}</td>
                <td>${lead.phone_work}</td>
                <td
                hx-get="/lead/${lead.id}/edit"
                hx-trigger="click"
                hx-swap="innerHTML"
                hx-target="#lead-${lead.id}"
                style="background-color: blue; color: white;"
                >
                    Edit
                </td>

    `);
});


app.post("/lead/:id/edit", async (req, res) => {
    const lead = await Lead.findById(req.params.id);
    const { first_name, last_name, phone_work } = req.body;
    lead.first_name = first_name || lead.first_name;
    lead.last_name = last_name || lead.last_name;
    lead.phone_work = phone_work || lead.phone_work;
    await lead.save();
    res.send(lead);
});


const PORT = process.env.PORT || 5000;

app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
