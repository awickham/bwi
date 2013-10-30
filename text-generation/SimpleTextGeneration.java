package textGeneration;

import java.io.IOException;
import java.io.InputStream;
import java.util.List;

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
	static final String QUERY = "Camera";

	public static void main(String[] args) throws IOException {
		// Read the ontology model from camera.owl.
		OntModel model = ModelFactory.createOntologyModel();
		InputStream in = FileManager.get().open( inputFileName );
		if (in == null) {
		    throw new IllegalArgumentException("File: " + inputFileName + " not found");
		}
		model.read(in, null);
		
		// List information about the given query.
		OntClass queryClass = model.getOntClass(modelNameSpace + QUERY);
		if(queryClass == null) {
			System.out.println("Could not find information about " + QUERY);
			System.exit(0);
		}
		ExtendedIterator<OntClass> subClassesIter = queryClass.listSubClasses(true);
		ExtendedIterator<OntClass> superClassesIter = queryClass.listSuperClasses(true);
		ExtendedIterator<OntProperty> propertiesIter = queryClass.listDeclaredProperties(true);
		//listClasses(subClassesIter, "subclass");
		//listClasses(superClassesIter, "super class");
		//listProperties(propertiesIter);
		generateSentence(subClassesIter, superClassesIter, propertiesIter);
	}

	/**
	 * List classes that relate to the query.
	 * @param iter the iterator over classes to print.
	 * @param classType the type of class in relation to the query (i.e. subclass or superclass).
	 */
	private static void listClasses(ExtendedIterator<OntClass> iter, String classType) {
		if(iter.hasNext()) {
			while(iter.hasNext()) {
				System.out.println(iter.next().getLocalName() + " is a " + classType + " of " + QUERY);
			}
		} else {
			System.out.println("No class is a " + classType + " of " + QUERY);
		}
		System.out.println();
	}

	/**
	 * List properties that relate to the query.
	 * @param iter the iterator over classes to print.
	 * @param classType the type of class in relation to the query (i.e. subclass or superclass).
	 */
	private static void listProperties(ExtendedIterator<OntProperty> iter) {
		if(iter.hasNext()) {
			while(iter.hasNext()) {
				System.out.println(QUERY + " has property " + iter.next().getLocalName());
			}
		} else {
			System.out.println(QUERY + " has no properties");
		}
		System.out.println();
	}

	/**
	 * Generate a simple sentence based on sub classes, super classes, and properties of the query.
	 */
	private static void generateSentence(
			ExtendedIterator<OntClass> subClassesIter,
			ExtendedIterator<OntClass> superClassesIter,
			ExtendedIterator<OntProperty> propertiesIter) {
		System.out.print("A " + QUERY.toLowerCase() + " is a ");
		listIter(superClassesIter);
		System.out.print(" with a ");
		listIter(propertiesIter);
		System.out.print(". ");
		listIter(subClassesIter);
		if(subClassesIter.toList().size() == 1) {
			System.out.print(" is an example of a " + QUERY.toLowerCase());
		} else {
			System.out.print(" are examples of " + QUERY.toLowerCase());
		}
		System.out.println(".");
	}

	/**
	 * Print out the elements in the iterator in natural language.
	 * Example: [viewFinder, body, lens] -> "viewFinder, body and lens"
	 * @param superClassesIter
	 */
	private static void listIter(ExtendedIterator<? extends OntResource> iter) {
		List<? extends OntResource> l = iter.toList();
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
