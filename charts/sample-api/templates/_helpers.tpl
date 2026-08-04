{{/* Expand the chart name. */}}
{{- define "sample-api.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/* Create a fully qualified application name. */}}
{{- define "sample-api.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{/* Chart label. */}}
{{- define "sample-api.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/* Selector labels are immutable for the Deployment. */}}
{{- define "sample-api.selectorLabels" -}}
app.kubernetes.io/name: {{ include "sample-api.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/* Common labels. */}}
{{- define "sample-api.labels" -}}
helm.sh/chart: {{ include "sample-api.chart" . }}
{{ include "sample-api.selectorLabels" . }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
app.kubernetes.io/component: api
app.kubernetes.io/part-of: enterprise-aks-gitops-platform
{{- end }}

{{/* Service account name. */}}
{{- define "sample-api.serviceAccountName" -}}
{{- if .Values.serviceAccount.create }}
{{- default (include "sample-api.fullname" .) .Values.serviceAccount.name }}
{{- else }}
{{- default "default" .Values.serviceAccount.name }}
{{- end }}
{{- end }}

{{/* Image reference. Digest wins over tag. */}}
{{- define "sample-api.image" -}}
{{- $repository := required "image.repository is required" .Values.image.repository -}}
{{- if .Values.image.digest -}}
{{- printf "%s@%s" $repository .Values.image.digest -}}
{{- else -}}
{{- $tag := default .Chart.AppVersion .Values.image.tag -}}
{{- printf "%s:%s" $repository $tag -}}
{{- end -}}
{{- end }}

{{/* Render Azure Key Vault object configuration for the CSI provider. */}}
{{- define "sample-api.keyVaultObjects" -}}
array:
{{ range .Values.azureKeyVault.objects }}
  - |
    objectName: {{ .objectName | quote }}
    objectType: "secret"
    objectVersion: {{ default "" .objectVersion | quote }}
{{ with .objectAlias }}
    objectAlias: {{ . | quote }}
{{ end }}
{{ end }}
{{- end }}

{{/* OpenTelemetry Collector labels. */}}
{{- define "sample-api.collectorLabels" -}}
helm.sh/chart: {{ include "sample-api.chart" . }}
app.kubernetes.io/name: {{ include "sample-api.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/version: {{ .Values.observability.collector.image.tag | quote }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
app.kubernetes.io/component: otel-collector
app.kubernetes.io/part-of: enterprise-aks-gitops-platform
{{- end }}

{{/* OpenTelemetry Collector selector labels. */}}
{{- define "sample-api.collectorSelectorLabels" -}}
app.kubernetes.io/name: {{ include "sample-api.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/component: otel-collector
{{- end }}

{{/* OpenTelemetry Collector image reference. */}}
{{- define "sample-api.collectorImage" -}}
{{- $repository := required "observability.collector.image.repository is required" .Values.observability.collector.image.repository -}}
{{- if .Values.observability.collector.image.digest -}}
{{- printf "%s@%s" $repository .Values.observability.collector.image.digest -}}
{{- else -}}
{{- printf "%s:%s" $repository (required "observability.collector.image.tag is required" .Values.observability.collector.image.tag) -}}
{{- end -}}
{{- end }}
