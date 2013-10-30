package textGeneration;

import java.io.IOException;
import java.io.InputStream;
import java.util.List;
import java.util.Scanner;

import com.hp.hpl.jena.ontology.OntClass;
import com.hp.hpl.jena.ontology.OntModel;
import com.hp.hpl.jena.ontology.OntProperty;
import com.hp.hpl.jena.ontology.OntResource;
import com.hp.hpl.jena.rdf.model.ModelFactory;
import com.hp.hpl.jena.util.FileManager;
import com.hp.hpl.jena.util.iterator.ExtendedIterator;

import simplenlg.aggregation.ClauseCoordinationRule;
import simplenlg.framework.*;
import simplenlg.lexicon.*;
import simplenlg.realiser.english.*;
import simplenlg.phrasespec.*;
import simplenlg.features.*;

public class SimpleTextGeneration {
	static final String inputFileName  = "camera.owl";
	static final String modelNameSpace = "http://www.xfront.com/owl/ontologies/camera/#";

	public static void main(String[] args) throws IOException {
		// Read the ontology model from camera.owl.
		OntModel model = ModelFactory.createOntologyModel();
		InputStream in = FileManager.get().open( inputFileName );
		if (in == null) {
		    throw new IllegalArgumentException("File: " + inputFileName + " not found");
		}
		model.read(in, null);
		
		// Prompt user to query the ontology, and answer in natural language.
		Scanner s = new Scanner(System.in);
		String query = "";
		System.out.print("Enter a query: ");
		while(!(query = s.nextLine()).equals("exit")) {
			OntClass queryClass = model.getOntClass(modelNameSpace + query);
			if(queryClass == null) {
				System.err.println("Could not find information about " + query);
			} else {
				List<OntClass> subClassesIter = queryClass.listSubClasses(true).toList();
				List<OntClass> superClassesIter = queryClass.listSuperClasses(true).toList();
				List<OntProperty> propertiesIter = queryClass.listDeclaredProperties(true).toList();
				generateSentence(subClassesIter, superClassesIter, propertiesIter, query);
			}
			System.out.print("Enter another query, or \"exit\" to exit: ");
		}
		s.close();
		System.out.println("Goodbye.");
	}

	/**
	 * Generate a simple sentence based on sub classes, super classes, and properties of the query.
	 */
	private static void generateSentence(List<OntClass> subClasses, List<OntClass> superClasses,
											List<OntProperty> properties, String query) {
		System.out.print("A " + query + " is a type of ");
		listIter(superClasses);
		if(properties.size() > 0) {
			System.out.print(" with a ");
			listIter(properties);
		}
		if(subClasses.size() > 0) {
			System.out.print(". ");
			listIter(subClasses);
			if(subClasses.size() == 1) {
				System.out.print(" is an example of a " + query);
			} else {
				System.out.print(" are examples of " + query);
			}
		}
		System.out.println(".");
	}

	/**
	 * Print out the elements in the iterator in natural language.
	 * Example: [viewFinder, body, lens] -> "viewFinder, body and lens"
	 * @param superClassesIter
	 */
	private static void listIter(List<? extends OntResource> l) {
		for(int i = 0; i < l.size(); i++) {
			System.out.print(l.get(i).getLocalName());
			if(l.size() >= 2 && i == l.size() - 2) {
				System.out.print(" and ");
			}
			else if(i < l.size() - 1) {
				System.out.print(", ");
			}
		}
	}
}
