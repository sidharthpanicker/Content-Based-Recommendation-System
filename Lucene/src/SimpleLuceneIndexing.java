import org.apache.lucene.analysis.standard.StandardAnalyzer;
import org.apache.lucene.document.Document;
import org.apache.lucene.document.Field;
import org.apache.lucene.document.StringField;
import org.apache.lucene.document.TextField;
import org.apache.lucene.index.DirectoryReader;
import org.apache.lucene.index.IndexReader;
import org.apache.lucene.index.IndexWriter;
import org.apache.lucene.index.IndexWriterConfig;
import org.apache.lucene.queryparser.classic.ParseException;
import org.apache.lucene.queryparser.classic.QueryParser;
import org.apache.lucene.search.IndexSearcher;
import org.apache.lucene.search.Query;
import org.apache.lucene.search.ScoreDoc;
import org.apache.lucene.search.TopScoreDocCollector;
import org.apache.lucene.store.Directory;
import org.apache.lucene.store.RAMDirectory;
import org.jsoup.Jsoup;
import org.jsoup.safety.Whitelist;
import org.jsoup.select.Elements;

import com.sun.xml.internal.ws.util.StringUtils;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.Scanner;

/**
 * Lucene Demo: basic similarity based content indexing
 * 
 * @author Sharonpova Current sample files fragments of wikibooks and
 *         stackoverflow.
 */

public class SimpleLuceneIndexing {

	private static void indexDirectory(IndexWriter writer, File dir) throws IOException {
		File[] files = dir.listFiles();
		for (int i = 0; i < files.length; i++) {
			File f = files[i];
			if (f.isDirectory()) {
				indexDirectory(writer, f); // recurse
			} else if (f.getName().endsWith(".txt")) {
				// call indexFile to add the title of the txt file to your index (you can also
				// index html)
				indexFile(writer, f);
			}
		}
	}

	private static void indexFile(IndexWriter writer, File f) throws IOException {
		System.out.println("Indexing " + f.getName());
		Document doc = new Document();
		doc.add(new TextField("filename", f.getName(), TextField.Store.YES));

		// open each file to index the content
		try {

			FileInputStream is = new FileInputStream(f);
			BufferedReader reader = new BufferedReader(new InputStreamReader(is));
			StringBuffer stringBuffer = new StringBuffer();
			String line = null;
			while ((line = reader.readLine()) != null) {
				stringBuffer.append(line).append("\n");
			}
			reader.close();
			doc.add(new TextField("contents", stringBuffer.toString(), TextField.Store.YES));

		} catch (Exception e) {

			System.out.println("something wrong with indexing content of the files");
		}
		writer.addDocument(doc);
	}

	public static void givenWritingStringToFile(String fileName, String str) throws IOException {
		FileOutputStream outputStream = new FileOutputStream("Website/" + fileName + ".txt");
		byte[] strToBytes = str.getBytes();
		outputStream.write(strToBytes);

		outputStream.close();
	}

	public static void scrapeData() {
		try {
			org.jsoup.nodes.Document document = Jsoup.connect("https://en.wikibooks.org/wiki/Java_Programming").get();
			org.jsoup.nodes.Document document2 = Jsoup.connect("https://docs.oracle.com/javase/tutorial/").get();
			Elements links = document.select("div#mw-content-text").select("a[href]");
			links.addAll(document2.select("div#TutBody").select("a[href]"));
			for (org.jsoup.nodes.Element link : links) {
				String attr = link.absUrl("href");
				String text = link.text();
				System.out.println(text);
				if (text != null) {
					try {
						if (attr.contains("jpg") || attr.contains("pdf")) {
							continue;
						}
						org.jsoup.nodes.Document dm = Jsoup.connect(attr).get();
						org.jsoup.nodes.Element htmlPage = dm.select("body").first();

		                String cleanedText = htmlPage.text();
						if (text.isEmpty() || text == null || text == "") {
							text = dm.title();
						}
						text = text.replaceAll("[^a-zA-Z]+", " ");
						Whitelist wl = Whitelist.simpleText();
						wl.addTags("style");
						String clean = Jsoup.clean(dm.body().toString(), wl);
						givenWritingStringToFile(text.trim(), cleanedText);
					} catch (Exception e) {
						// e.printStackTrace();
						continue;
					}
				}
				
			}
		} catch (IOException e) {
			e.printStackTrace();
		}
	}

	
	/* public static void main(String[] args) throws IOException, ParseException {
	 scrapeData(); 
	 }*/
	 
	public static void main(String[] args) throws IOException, ParseException {
		
		File file = new File("Website");
		if(file.isDirectory()){
			System.out.println("Is Directory");
			System.out.println(file.list().length);
			if(file.list().length < 2){
				scrapeData();
			}else{
				// TO DO
			}	
		}else{
			System.out.println("This is not a directory");
		}
		
		//scrapeData();
		File dataDir = new File("Website"); // my sample file folder path
		// Check whether the directory to be indexed exists
		if (!dataDir.exists() || !dataDir.isDirectory()) {
			throw new IOException(dataDir + " does not exist or is not a directory");
		}
		Directory indexDir = new RAMDirectory();

		// Specify the analyzer for tokenizing text.
		StandardAnalyzer analyzer = new StandardAnalyzer();
		IndexWriterConfig config = new IndexWriterConfig(analyzer);
		IndexWriter writer = new IndexWriter(indexDir, config);

		// call indexDirectory to add to your index
		// the names of the txt files in dataDir
		indexDirectory(writer, dataDir);
		writer.close();

		// Query string!
		String querystr = "contents:Null Pointer Exception";
		querystr = args[0];

		// This is going to be your selected posts.
		Scanner console = new Scanner(System.in);
		// String querystr = "contents:"+console.nextLine();
		System.out.println(querystr);

		Query q = new QueryParser("contents", analyzer).parse(querystr);
		int hitsPerPage = 10;
		IndexReader reader = null;

		TopScoreDocCollector collector = null;
		IndexSearcher searcher = null;
		reader = DirectoryReader.open(indexDir);
		searcher = new IndexSearcher(reader);
		collector = TopScoreDocCollector.create(hitsPerPage);
		searcher.search(q, collector);

		ScoreDoc[] hits = collector.topDocs().scoreDocs;
		System.out.println("Found " + hits.length + " hits.");
		//System.out.println();

		for (int i = 0; i < hits.length; ++i) {
			int docId = hits[i].doc;
			Document d;
			d = searcher.doc(docId);

			System.out.println((i + 1) + ". " + d.get("filename"));
		}
		reader.close();
	}

}