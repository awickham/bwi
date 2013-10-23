package textGeneration;

import java.io.IOException;
import java.io.InputStream;

import com.hp.hpl.jena.ontology.OntClass;
import com.hp.hpl.jena.ontology.OntModel;
import com.hp.hpl.jena.ontology.OntProperty;
import com.hp.hpl.jena.rdf.model.ModelFactory;
import com.hp.hpl.jena.util.FileManager;
import com.hp.hpl.jena.util.iterator.ExtendedIterator;

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
		ExtendedIterator<OntClass> subClassesIter = queryClass.listSubClasses(true);
		ExtendedIterator<OntClass> superClassesIter = queryClass.listSuperClasses(true);
		ExtendedIterator<OntProperty> propertiesIter = queryClass.listDeclaredProperties(true);
		listClasses(subClassesIter, "subclass");
		listClasses(superClassesIter, "super class");
		listProperties(propertiesIter);
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
}
