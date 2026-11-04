<?xml version='1.0' encoding='UTF-8'?>
<Project Type="Project" LVVersion="26008000">
	<Property Name="CCSymbols" Type="Str"></Property>
	<Property Name="NI.LV.All.SaveVersion" Type="Str">26.0</Property>
	<Property Name="NI.LV.All.SourceOnly" Type="Bool">true</Property>
	<Property Name="NI.Project.Description" Type="Str"></Property>
	<Item Name="My Computer" Type="My Computer">
		<Property Name="NI.SortType" Type="Int">3</Property>
		<Property Name="server.app.propertiesEnabled" Type="Bool">true</Property>
		<Property Name="server.control.propertiesEnabled" Type="Bool">true</Property>
		<Property Name="server.tcp.enabled" Type="Bool">false</Property>
		<Property Name="server.tcp.port" Type="Int">0</Property>
		<Property Name="server.tcp.serviceName" Type="Str">My Computer/VI Server</Property>
		<Property Name="server.tcp.serviceName.default" Type="Str">My Computer/VI Server</Property>
		<Property Name="server.vi.callsEnabled" Type="Bool">true</Property>
		<Property Name="server.vi.propertiesEnabled" Type="Bool">true</Property>
		<Property Name="specify.custom.address" Type="Bool">false</Property>
		<Item Name="Actors" Type="Folder">
			<Item Name="Console Logger.lvlib" Type="Library" URL="../Actors/Console Logger/Console Logger.lvlib"/>
			<Item Name="Runner.lvlib" Type="Library" URL="../Actors/Runner/Runner.lvlib"/>
			<Item Name="UI Logger.lvlib" Type="Library" URL="../Actors/UI Logger/UI Logger.lvlib"/>
			<Item Name="File Logger.lvlib" Type="Library" URL="../Actors/File Logger/File Logger.lvlib"/>
			<Item Name="Mock Logger.lvlib" Type="Library" URL="../Actors/Mock Logger/Mock Logger.lvlib"/>
		</Item>
		<Item Name="Classes" Type="Folder">
			<Property Name="NI.SortType" Type="Int">0</Property>
			<Item Name="Array.lvclass" Type="LVClass" URL="../Classes/Array/Array.lvclass"/>
			<Item Name="Boolean.lvclass" Type="LVClass" URL="../Classes/Boolean/Boolean.lvclass"/>
			<Item Name="Cluster.lvclass" Type="LVClass" URL="../Classes/Cluster/Cluster.lvclass"/>
			<Item Name="Element Manager.lvclass" Type="LVClass" URL="../Classes/Element Manager/Element Manager.lvclass"/>
			<Item Name="Element.lvclass" Type="LVClass" URL="../Classes/Element/Element.lvclass"/>
			<Item Name="File Manager.lvclass" Type="LVClass" URL="../Classes/File Manager/File Manager.lvclass"/>
			<Item Name="Hash Whitelist Handler.lvclass" Type="LVClass" URL="../Classes/Hash Whitelist Handler/Hash Whitelist Handler.lvclass"/>
			<Item Name="LabVIEW File.lvclass" Type="LVClass" URL="../Classes/LabVIEW File/LabVIEW File.lvclass"/>
			<Item Name="LV File Creator.lvclass" Type="LVClass" URL="../Classes/LV File Creator/LV File Creator.lvclass"/>
			<Item Name="Numeric.lvclass" Type="LVClass" URL="../Classes/Numeric/Numeric.lvclass"/>
			<Item Name="Project Manager.lvclass" Type="LVClass" URL="../Classes/Project Manager/Project Manager.lvclass"/>
			<Item Name="Python Caller.lvclass" Type="LVClass" URL="../Classes/Python Caller/Python Caller.lvclass"/>
			<Item Name="String.lvclass" Type="LVClass" URL="../Classes/String/String.lvclass"/>
			<Item Name="Type Definition.lvclass" Type="LVClass" URL="../Classes/Type Definition/Type Definition.lvclass"/>
			<Item Name="Virtual Instrument.lvclass" Type="LVClass" URL="../Classes/Virtual Instrument/Virtual Instrument.lvclass"/>
		</Item>
		<Item Name="Constants" Type="Folder">
			<Property Name="NI.SortType" Type="Int">0</Property>
			<Item Name="Blue Options--constant.vi" Type="VI" URL="../Constants/Blue Options--constant.vi"/>
			<Item Name="Environment Variable for Main venv--constant.vi" Type="VI" URL="../Constants/Environment Variable for Main venv--constant.vi"/>
			<Item Name="Environment Variable for PPL venv--constant.vi" Type="VI" URL="../Constants/Environment Variable for PPL venv--constant.vi"/>
			<Item Name="File Name of Python Adapter--constant.vi" Type="VI" URL="../Constants/File Name of Python Adapter--constant.vi"/>
			<Item Name="File Name of Python Module--constant.vi" Type="VI" URL="../Constants/File Name of Python Module--constant.vi"/>
			<Item Name="Function Name String Constant Label--constant.vi" Type="VI" URL="../Constants/Function Name String Constant Label--constant.vi"/>
			<Item Name="G-CLI Help Message--constant.vi" Type="VI" URL="../Constants/G-CLI Help Message--constant.vi"/>
			<Item Name="G-CLI Parameters--constant.vi" Type="VI" URL="../Constants/G-CLI Parameters--constant.vi"/>
			<Item Name="Hash Whitelist--constant.vi" Type="VI" URL="../Constants/Hash Whitelist--constant.vi"/>
			<Item Name="Label of Cluster in Type Definition Template--constant.vi" Type="VI" URL="../Constants/Label of Cluster in Type Definition Template--constant.vi"/>
			<Item Name="Label of File Name Array in Hash List--constant.vi" Type="VI" URL="../Constants/Label of File Name Array in Hash List--constant.vi"/>
			<Item Name="Label of Hash Value Array in Hash List--constant.vi" Type="VI" URL="../Constants/Label of Hash Value Array in Hash List--constant.vi"/>
			<Item Name="Library Template Name--constant.vi" Type="VI" URL="../Constants/Library Template Name--constant.vi"/>
			<Item Name="Name of Build Specification--constant.vi" Type="VI" URL="../Constants/Name of Build Specification--constant.vi"/>
			<Item Name="Output Parameter Type Constant Label--constant.vi" Type="VI" URL="../Constants/Output Parameter Type Constant Label--constant.vi"/>
			<Item Name="Suffix Duplicated VI--constant.vi" Type="VI" URL="../Constants/Suffix Duplicated VI--constant.vi"/>
			<Item Name="Template Project Name--constant.vi" Type="VI" URL="../Constants/Template Project Name--constant.vi"/>
			<Item Name="Type Definition Folder Name--constant.vi" Type="VI" URL="../Constants/Type Definition Folder Name--constant.vi"/>
			<Item Name="Type Definition Template Name--constant.vi" Type="VI" URL="../Constants/Type Definition Template Name--constant.vi"/>
			<Item Name="VI Template Name--constant.vi" Type="VI" URL="../Constants/VI Template Name--constant.vi"/>
			<Item Name="Whitelist File Name--constant.vi" Type="VI" URL="../Constants/Whitelist File Name--constant.vi"/>
		</Item>
		<Item Name="Custom Errors" Type="Folder">
			<Property Name="NI.SortType" Type="Int">0</Property>
			<Item Name="File execution not authorized--error.vi" Type="VI" URL="../Custom Errors/File execution not authorized--error.vi"/>
			<Item Name="Invalid Data Type--error.vi" Type="VI" URL="../Custom Errors/Invalid Data Type--error.vi"/>
			<Item Name="Invalid Environment Variable--error.vi" Type="VI" URL="../Custom Errors/Invalid Environment Variable--error.vi"/>
			<Item Name="Invalid project element extension--error.vi" Type="VI" URL="../Custom Errors/Invalid project element extension--error.vi"/>
			<Item Name="Invalid Venv Path--error.vi" Type="VI" URL="../Custom Errors/Invalid Venv Path--error.vi"/>
			<Item Name="LabVIEW CLI argument missing--error.vi" Type="VI" URL="../Custom Errors/LabVIEW CLI argument missing--error.vi"/>
			<Item Name="New root not relative--error.vi" Type="VI" URL="../Custom Errors/New root not relative--error.vi"/>
			<Item Name="Project Item Not Found--error.vi" Type="VI" URL="../Custom Errors/Project Item Not Found--error.vi"/>
			<Item Name="Python executable does not exist--error.vi" Type="VI" URL="../Custom Errors/Python executable does not exist--error.vi"/>
			<Item Name="Target must be a directory--error.vi" Type="VI" URL="../Custom Errors/Target must be a directory--error.vi"/>
		</Item>
		<Item Name="Interfaces" Type="Folder">
			<Property Name="NI.SortType" Type="Int">0</Property>
			<Item Name="IElement Manager.lvclass" Type="LVClass" URL="../Interfaces/IElement Manager/IElement Manager.lvclass"/>
			<Item Name="IElement.lvclass" Type="LVClass" URL="../Interfaces/IElement/IElement.lvclass"/>
			<Item Name="IFile Manager.lvclass" Type="LVClass" URL="../Interfaces/IFile Manager/IFile Manager.lvclass"/>
			<Item Name="IHash Whitelist Handler.lvclass" Type="LVClass" URL="../Interfaces/IHash Whitelist Handler/IHash Whitelist Handler.lvclass"/>
			<Item Name="ILabVIEW File.lvclass" Type="LVClass" URL="../Interfaces/ILabVIEW File/ILabVIEW File.lvclass"/>
			<Item Name="ILogger Client.lvlib" Type="Library" URL="../Interfaces/ILogger Client/ILogger Client.lvlib"/>
			<Item Name="ILogger.lvlib" Type="Library" URL="../Interfaces/ILogger/ILogger.lvlib"/>
			<Item Name="ILV File Creator.lvclass" Type="LVClass" URL="../Interfaces/ILV File Creator/ILV File Creator.lvclass"/>
			<Item Name="IProject Manager.lvclass" Type="LVClass" URL="../Interfaces/IProject Manager/IProject Manager.lvclass"/>
			<Item Name="IPython Caller.lvclass" Type="LVClass" URL="../Interfaces/IPython Caller/IPython Caller.lvclass"/>
			<Item Name="IRunner.lvlib" Type="Library" URL="../Interfaces/IRunner/IRunner.lvlib"/>
		</Item>
		<Item Name="Launchers" Type="Folder">
			<Item Name="py2vi.vi" Type="VI" URL="../Launchers/py2vi.vi"/>
			<Item Name="Launch in IDE.vi" Type="VI" URL="../Launchers/Launch in IDE.vi"/>
			<Item Name="py2vi-lvcli.vi" Type="VI" URL="../Launchers/py2vi-lvcli.vi"/>
		</Item>
		<Item Name="Mocks" Type="Folder">
			<Item Name="Mock IFile Manager.lvclass" Type="LVClass" URL="../Mocks/Mock IFile Manager/Mock IFile Manager.lvclass"/>
			<Item Name="Mock IPython Caller.lvclass" Type="LVClass" URL="../Mocks/Mock IPython Caller/Mock IPython Caller.lvclass"/>
			<Item Name="Mock IProject Manager.lvclass" Type="LVClass" URL="../Mocks/Mock IProject Manager/Mock IProject Manager.lvclass"/>
		</Item>
		<Item Name="Support" Type="Folder">
			<Property Name="NI.SortType" Type="Int">0</Property>
			<Item Name="Add String to Array Constant.vi" Type="VI" URL="../Support/Add String to Array Constant.vi"/>
			<Item Name="Add Suffix to File Name.vi" Type="VI" URL="../Support/Add Suffix to File Name.vi"/>
			<Item Name="File Integrity Guard.vi" Type="VI" URL="../Support/File Integrity Guard.vi"/>
			<Item Name="Filter Subfolders.vi" Type="VI" URL="../Support/Filter Subfolders.vi"/>
			<Item Name="Generate Log Entry.vi" Type="VI" URL="../Support/Generate Log Entry.vi"/>
			<Item Name="Generate Parameters Typedef Name.vi" Type="VI" URL="../Support/Generate Parameters Typedef Name.vi"/>
			<Item Name="Generate Paths And Strings.vi" Type="VI" URL="../Type Definitions/Generate Paths And Strings.vi"/>
			<Item Name="Generate Type Definition Filename.vi" Type="VI" URL="../Support/Generate Type Definition Filename.vi"/>
			<Item Name="Generate VI Name.vi" Type="VI" URL="../Support/Generate VI Name.vi"/>
			<Item Name="Get Python Version from Venv.vi" Type="VI" URL="../Support/Get Python Version from Venv.vi"/>
			<Item Name="Index Project Item by Name.vi" Type="VI" URL="../Classes/Project Manager/Index Project Item by Name.vi"/>
			<Item Name="Initialize Interfaces for Runner.vi" Type="VI" URL="../Support/Initialize Interfaces for Runner.vi"/>
			<Item Name="Make Path Relative.vi" Type="VI" URL="../Support/Make Path Relative.vi"/>
			<Item Name="Open Venv Session.vi" Type="VI" URL="../Support/Open Venv Session.vi"/>
			<Item Name="Parse LabVIEWCLI Argument.vi" Type="VI" URL="../Support/Parse LabVIEWCLI Argument.vi"/>
			<Item Name="Read Environment Variable.vi" Type="VI" URL="../Support/Read Environment Variable.vi"/>
			<Item Name="Shorten Path for Display.vi" Type="VI" URL="../Support/Shorten Path for Display.vi"/>
			<Item Name="String to Build Version.vi" Type="VI" URL="../Support/String to Build Version.vi"/>
		</Item>
		<Item Name="Tests" Type="Folder">
			<Item Name="Analyze Dummy Module.vi" Type="VI" URL="../Tests/Analyze Dummy Module.vi"/>
			<Item Name="Generate VI Names.lvclass" Type="LVClass" URL="../Tests/Generate VI Names/Generate VI Names.lvclass"/>
			<Item Name="Python Code Analysis.lvclass" Type="LVClass" URL="../Tests/Python Code Analysis/Python Code Analysis.lvclass"/>
			<Item Name="Support VIs.lvclass" Type="LVClass" URL="../Tests/Support VIs/Support VIs.lvclass"/>
			<Item Name="Runner Unit Test - Prepare Project.lvclass" Type="LVClass" URL="../Tests/Runner Unit Test - Prepare Project/Runner Unit Test - Prepare Project.lvclass"/>
			<Item Name="Runner Unit Test - Process Python Code.lvclass" Type="LVClass" URL="../Tests/Runner Unit Test - Process Python Code/Runner Unit Test - Process Python Code.lvclass"/>
			<Item Name="Runner Unit Test - Create Files.lvclass" Type="LVClass" URL="../Tests/Runner Unit Test - Create Files/Runner Unit Test - Create Files.lvclass"/>
			<Item Name="Runner Unit Test - Clean Project.lvclass" Type="LVClass" URL="../Tests/Runner Unit Test - Clean Project/Runner Unit Test - Clean Project.lvclass"/>
			<Item Name="Runner Unit Test - Add Files to Project.lvclass" Type="LVClass" URL="../Tests/Runner Unit Test - Add Files to Project/Runner Unit Test - Add Files to Project.lvclass"/>
		</Item>
		<Item Name="Type Definitions" Type="Folder">
			<Item Name="Analysis Output--cluster.ctl" Type="VI" URL="../Type Definitions/Analysis Output--cluster.ctl"/>
			<Item Name="Containers--enum.ctl" Type="VI" URL="../Type Definitions/Containers--enum.ctl"/>
			<Item Name="Data types--enum.ctl" Type="VI" URL="../Type Definitions/Data types--enum.ctl"/>
			<Item Name="Function--cluster.ctl" Type="VI" URL="../Type Definitions/Function--cluster.ctl"/>
			<Item Name="Log Entry--cluster.ctl" Type="VI" URL="../Type Definitions/Log Entry--cluster.ctl"/>
			<Item Name="Parameter Mode--enum.ctl" Type="VI" URL="../Type Definitions/Parameter Mode--enum.ctl"/>
			<Item Name="Parameter--cluster.ctl" Type="VI" URL="../Type Definitions/Parameter--cluster.ctl"/>
			<Item Name="Paths And Strings--cluster.ctl" Type="VI" URL="../Type Definitions/Paths And Strings--cluster.ctl"/>
			<Item Name="Type Definition--cluster.ctl" Type="VI" URL="../Type Definitions/Type Definition--cluster.ctl"/>
			<Item Name="Type Definition Template--cluster.ctl" Type="VI" URL="../Type Definitions/Type Definition Template--cluster.ctl"/>
		</Item>
		<Item Name="Function VI Template.vi" Type="VI" URL="../Function VI Template.vi"/>
		<Item Name="Package Dependencies" Type="IIO Ladder Diagram">
			<Property Name="NI.SortType" Type="Int">0</Property>
		</Item>
		<Item Name="Dependencies" Type="Dependencies"/>
		<Item Name="Build Specifications" Type="Build"/>
	</Item>
</Project>
