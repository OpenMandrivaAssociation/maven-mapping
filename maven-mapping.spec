Name:		maven-mapping
Version:	3.0.0
Release:	1
Summary:	Map a Maven artifact to a file name
Group:		Development/Java
License:	Apache-2.0
URL:		https://maven.apache.org/shared/maven-mapping/
Source0:	https://github.com/apache/maven-mapping/archive/refs/tags/maven-mapping-%{version}.tar.gz#/maven-mapping-%{version}.tar.gz
BuildArch:	noarch
BuildRequires:	python
BuildRequires:	maven
BuildRequires:	maven-components >= 3.10.0
BuildRequires:	java-current-devel
BuildRequires:	mvn(org.apache.maven:maven-artifact)
BuildRequires:	mvn(org.codehaus.plexus:plexus-utils)
BuildRequires:	plexus-utils >= 3.6.2
BuildRequires:	mvn(org.codehaus.plexus:plexus-interpolation)
BuildRequires:	plexus-interpolation >= 1.30.0
Requires:	plexus-interpolation >= 1.30.0
BuildSystem:	maven
BuildOption(install):	--file-name %{name}

%description
Turns an artifact mapping pattern into a file name. 3.0.0 interpolates
group, artifact, version, classifier, and extension through
plexus-interpolation 1.30. The sources use maven-artifact, not
maven-core. Tests are not run.

%prep
%autosetup -n maven-mapping-maven-mapping-%{version}
rm -rf src/test src/site
python - <<'PY'
import xml.etree.ElementTree as ET
NS = "http://maven.apache.org/POM/4.0.0"
ET.register_namespace("", NS)

def tag(name):
    return "{" + NS + "}" + name

def add(parent, name, text):
    node = ET.SubElement(parent, tag(name))
    node.text = text
    return node

root = ET.Element(tag("project"))
add(root, "modelVersion", "4.0.0")
add(root, "groupId", "org.apache.maven.shared")
add(root, "artifactId", "maven-mapping")
add(root, "version", "%{version}")
add(root, "name", "Apache Maven Mapping")
props = ET.SubElement(root, tag("properties"))
add(props, "maven.compiler.release", "8")
add(props, "project.build.sourceEncoding", "UTF-8")
deps = ET.SubElement(root, tag("dependencies"))
for group, artifact, version in (
    ("org.apache.maven", "maven-artifact", "3.10.0"),
    ("org.codehaus.plexus", "plexus-interpolation", "1.30.0"),
):
    dep = ET.SubElement(deps, tag("dependency"))
    add(dep, "groupId", group)
    add(dep, "artifactId", artifact)
    add(dep, "version", version)
ET.ElementTree(root).write("pom.xml", encoding="utf-8", xml_declaration=True)
PY

%files -f .mfiles
