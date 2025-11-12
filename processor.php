class XSLTProcessor {
/* Properties */
public bool $doXInclude = false;
public bool $cloneDocument = false;
public int $maxTemplateDepth;
public int $maxTemplateVars;
/* Methods */
public getParameter(string $namespace, string $name): string|false
public getSecurityPrefs(): int
public hasExsltSupport(): bool
public importStylesheet(object $stylesheet): bool
public registerPHPFunctionNS(string $namespaceURI, string $name, callable $callable): void
public registerPHPFunctions(array|string|null $functions = null): void
public removeParameter(string $namespace, string $name): bool
public setParameter(string $namespace, string $name, string $value): bool
public setParameter(string $namespace, array $options): bool
public setProfiling(?string $filename): true
public setSecurityPrefs(int $preferences): int
public transformToDoc(object $document, ?string $returnClass = null): object|false
public transformToUri(object $document, string $uri): int
public transformToXml(object $document): string|null|false
}
abstract class Dom\Document extends Dom\Node implements Dom\ParentNode {
/* Inherited constants */
public const int Dom\Node::DOCUMENT_POSITION_DISCONNECTED = 0x1;
public const int Dom\Node::DOCUMENT_POSITION_PRECEDING = 0x2;
public const int Dom\Node::DOCUMENT_POSITION_FOLLOWING = 0x4;
public const int Dom\Node::DOCUMENT_POSITION_CONTAINS = 0x8;
public const int Dom\Node::DOCUMENT_POSITION_CONTAINED_BY = 0x10;
public const int Dom\Node::DOCUMENT_POSITION_IMPLEMENTATION_SPECIFIC = 0x20;
/* Properties */
public readonly Dom\Implementation $implementation;
public string $URL;
public string $documentURI;
public string $characterSet;
public string $charset;
public string $inputEncoding;
public readonly ?Dom\DocumentType $doctype;
public readonly ?Dom\Element $documentElement;
public readonly ?Dom\Element $firstElementChild;
public readonly ?Dom\Element $lastElementChild;
public readonly int $childElementCount;
public ?Dom\HTMLElement $body;
public readonly ?Dom\HTMLElement $head;
public string $title;
/* Inherited properties */
public readonly int $nodeType;
public readonly string $nodeName;
public readonly string $baseURI;
public readonly bool $isConnected;
public readonly ?Dom\Document $ownerDocument;
public readonly ?Dom\Node $parentNode;
public readonly ?Dom\Element $parentElement;
public readonly Dom\NodeList $childNodes;
public readonly ?Dom\Node $firstChild;
public readonly ?Dom\Node $lastChild;
public readonly ?Dom\Node $previousSibling;
public readonly ?Dom\Node $nextSibling;
public ?string $nodeValue;
public ?string $textContent;
/* Methods */
/* Not documented yet */
/* Inherited methods */
/* Not documented yet */
}

class XMLReader {
/* Constants */
public const int NONE;
public const int ELEMENT;
public const int ATTRIBUTE;
public const int TEXT;
public const int CDATA;
public const int ENTITY_REF;
public const int ENTITY;
public const int PI;
public const int COMMENT;
public const int DOC;
public const int DOC_TYPE;
public const int DOC_FRAGMENT;
public const int NOTATION;
public const int WHITESPACE;
public const int SIGNIFICANT_WHITESPACE;
public const int END_ELEMENT;
public const int END_ENTITY;
public const int XML_DECLARATION;
public const int LOADDTD;
public const int DEFAULTATTRS;
public const int VALIDATE;
public const int SUBST_ENTITIES;
/* Properties */
public int $attributeCount;
public string $baseURI;
public int $depth;
public bool $hasAttributes;
public bool $hasValue;
public bool $isDefault;
public bool $isEmptyElement;
public string $localName;
public string $name;
public string $namespaceURI;
public int $nodeType;
public string $prefix;
public string $value;
public string $xmlLang;
/* Methods */
public close(): true
public expand(?DOMNode $baseNode = null): DOMNode|false
public static fromStream(
    resource $stream,
    ?string $encoding = null,
    int $flags = 0,
    ?string $documentUri = null
): static
public static fromString(string $source, ?string $encoding = null, int $flags = 0): static
public static fromUri(string $uri, ?string $encoding = null, int $flags = 0): static
public getAttribute(string $name): ?string
public getAttributeNo(int $index): ?string
public getAttributeNs(string $name, string $namespace): ?string
public getParserProperty(int $property): bool
public isValid(): bool
public lookupNamespace(string $prefix): ?string
public moveToAttribute(string $name): bool
public moveToAttributeNo(int $index): bool
public moveToAttributeNs(string $name, string $namespace): bool
public moveToElement(): bool
public moveToFirstAttribute(): bool
public moveToNextAttribute(): bool
public next(?string $name = null): bool
public static open(string $uri, ?string $encoding = null, int $flags = 0): XMLReader
public open(string $uri, ?string $encoding = null, int $flags = 0): bool
public read(): bool
public readInnerXml(): string
public readOuterXml(): string
public readString(): string
public setParserProperty(int $property, bool $value): bool
public setRelaxNGSchema(?string $filename): bool
public setRelaxNGSchemaSource(?string $source): bool
public setSchema(?string $filename): bool
public static XML(string $source, ?string $encoding = null, int $flags = 0): XMLReader
public XML(string $source, ?string $encoding = null, int $flags = 0): bool
}
