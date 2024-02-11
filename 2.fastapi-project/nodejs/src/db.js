import mongoose from 'mongoose';

const MONGO_URI = process.env.MONGO_URI || 'mongodb://127.0.0.1:27017/demo-db'

export const connectDB = async () => {
    try {
        const conn = await mongoose.connect(MONGO_URI);

        console.log(`MongoDB Connected: ${conn.connection.host}`);
    } catch (error) {
        console.error(`Error: ${error.message}`);
        process.exit(1);
    }
}


// TODO: Seperate models into their own files

const schema = new mongoose.Schema({
    first_name: {
        type: String,
        required: true
    },
    last_name: {
        type: String,
        required: true
    },
    phone_work: {
        type: String,
        required: true
    },
    id: {
        type: String,
        required: true
    }
});


export const Lead = mongoose.model('Lead', schema);
