import express from 'express';
import { MongoClient, Db } from 'mongodb';
import debugFactory from 'debug';
import morgan from 'morgan';

const debug = debugFactory('server');

const PORT = +process.env.PORT!;
const DB_HOST = process.env.DB_HOST;
const DB_PORT = process.env.DB_PORT;
const DB_NAME = process.env.DB_NAME;

const getDataFromDB = (() => {
    // Кеширование запросов
    let cache: Record<string, Array<any>> | null = null;
    return async function(db: Db) {
        if (cache) { 
            debug('get data from cache');

            return cache;
        }
        const commandCursor = db.listCollections();
        const data: Record<string, Array<any>> = {};
        while (await commandCursor.hasNext()) {
            const collectionInfo = (await commandCursor.next()) as { name: string };
            
            if (!collectionInfo) continue;
            
            const collection = db.collection(collectionInfo.name);

            debug('processing collection: %s', collectionInfo.name);

            const docs = await collection.find({}).toArray();
            
            data[collectionInfo.name] = docs;
        }
        cache = data;
        return data;
    }
})();

async function connectMongoClient() {
    const host = [[DB_HOST, DB_PORT].join(':'), DB_NAME].join('/');
    const url = ['mongodb', host].join('://');
    
    debug('db connection url: %s', url);

    const dbName = DB_NAME;
    const mongoClient = await MongoClient.connect(url, { useUnifiedTopology: true });
    const db = mongoClient.db(dbName);

    debug('db %s succesfully connected', dbName);

    return db;
}

async function main() {
    const app = express();

    app.use(morgan('dev'));

    const db = await connectMongoClient();

    app.get('/', async (_, res) => {
        const data = await getDataFromDB(db);
        res.json(data).end();
    });

    app.get('/health', async (_, res) => {
        res.status(200).end();
    });

    app.use((_, res) => {
        res.status(404).send('Resource not exists');
    });

    app.listen(PORT, () => {
        debug('server start listening on %d', PORT);
    });   
}

main().catch(error => { throw error });
